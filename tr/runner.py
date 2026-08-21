"""Rule 5: run the offline-deterministic snippets, mark the rest unverified.

Classification is a static text check, not an LLM call -- deterministic, free,
and wrong in only one direction (a false "live" just means a manual paste).
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BLOCK_RE = re.compile(r"```(?:python|py)\n(.*?)```", re.DOTALL)

# Anything here means the snippet reaches the network or a paid API.
LIVE_MARKERS = [
    "openai", "anthropic", "genai", "gemini", "cohere", "mistralai", "litellm",
    "langchain", "llama_index", "llamaindex", "ollama", "groq", "replicate",
    "requests.", "httpx.", "urllib.request", "aiohttp", "boto3",
    "api_key", "API_KEY", "from_pretrained", "huggingface_hub", "hf_hub",
    "pipeline(", "input(", "webbrowser", "socket.",
]


def is_live(code):
    low = code.lower()
    return any(m.lower() in low for m in LIVE_MARKERS)


def run_snippet(code, timeout):
    """Execute in a temp dir with the current interpreter. Returns a dict."""
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "snippet.py"
        script.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=timeout, cwd=tmp,
            )
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "out": "", "err": f"no exit within {timeout}s"}
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        missing = re.search(r"ModuleNotFoundError: No module named '([^']+)'", err)
        if missing:
            return {"status": "missing_dep", "out": out, "err": missing.group(1)}
        return {"status": "error", "out": out, "err": err}
    return {"status": "ok", "out": out, "err": err}


NO_EXEC_NOTE = (
    "\n\n> `[UNVERIFIED]` Code execution is off in this environment, so this\n"
    "> snippet was not run. Run it and paste your real output below.\n\n"
    "```text\n[UNVERIFIED - paste the output of your run]\n```\n"
)


def verify(markdown, timeout=30, execute=True):
    """Append a real-output block after every runnable snippet.

    `execute=False` runs nothing and marks every snippet unverified. That is the
    right setting anywhere the generated code should not be executed -- a hosted
    app runs on someone else's machine, and nobody has reviewed the model's code.

    Returns (new_markdown, results) where results is one dict per snippet.
    """
    results = []
    pieces, cursor = [], 0

    for n, m in enumerate(BLOCK_RE.finditer(markdown), 1):
        code = m.group(1)
        pieces.append(markdown[cursor:m.end()])
        cursor = m.end()

        if not execute:
            results.append({"n": n, "status": "not_executed", "err": ""})
            pieces.append(NO_EXEC_NOTE)
            continue

        if is_live(code):
            results.append({"n": n, "status": "live", "err": ""})
            pieces.append(
                "\n\n> `[UNVERIFIED]` This snippet calls a live model API, so the\n"
                "> output is not reproducible and was not generated here. Run it and\n"
                "> paste your real output below.\n\n"
                "```text\n[UNVERIFIED - paste the output of your run]\n```\n"
            )
            continue

        r = run_snippet(code, timeout)
        r["n"] = n
        results.append(r)

        if r["status"] == "ok":
            body = r["out"] if r["out"] else "(ran successfully, printed nothing)"
            pieces.append(f"\n\nOutput of a real run:\n\n```text\n{body}\n```\n")
        elif r["status"] == "missing_dep":
            pieces.append(
                f"\n\n> `[UNVERIFIED]` Could not run here: `{r['err']}` is not\n"
                f"> installed. Install it and re-run to capture the real output.\n\n"
                "```text\n[UNVERIFIED - paste the output of your run]\n```\n"
            )
        else:
            pieces.append(
                f"\n\n> `[UNVERIFIED]` This snippet failed to run ({r['status']}).\n"
                f"> Reported error, shown so it is not hidden:\n\n"
                f"```text\n{(r['err'] or 'no stderr')[:1500]}\n```\n"
            )

    pieces.append(markdown[cursor:])
    return "".join(pieces), results


def summarise(results):
    if not results:
        return "No python snippets found."
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    order = ["ok", "live", "not_executed", "missing_dep", "error", "timeout"]
    label = {
        "ok": "executed, real output inserted",
        "live": "live API call, marked UNVERIFIED",
        "not_executed": "not run (execution off here), marked UNVERIFIED",
        "missing_dep": "dependency missing, marked UNVERIFIED",
        "error": "failed to run, error shown",
        "timeout": "timed out, marked UNVERIFIED",
    }
    lines = [f"{len(results)} python snippet(s):"]
    for k in order:
        if k in counts:
            lines.append(f"- {counts[k]} {label[k]}")
    for r in results:
        if r["status"] in ("error", "timeout"):
            lines.append(f"  - snippet {r['n']}: {r['err'][:200]}")
    return "\n".join(lines)
