# Deploying the app

Two ways to run the same app. The engine is identical; only code execution and
where files are written differ.

| | Local | Streamlit Community Cloud |
|---|---|---|
| Command | `streamlit run app.py` | push to GitHub, deploy from there |
| API key | `OPENROUTER_API_KEY` in your shell | the app's **Secrets** box |
| Rule 5 code execution | On (real outputs) | **Off** (`[UNVERIFIED]` markers) |
| Output | download, or **Save to out/** | download only |
| Who can use it | you | anyone with the link, unless you restrict viewers |

---

## Run it locally

```
pip install -r requirements.txt
$env:OPENROUTER_API_KEY="sk-or-..."      # PowerShell
$env:TR_LOCAL="1"                        # enables code execution
streamlit run app.py
```

`TR_LOCAL=1` is what turns on Rule 5 execution. Without it the app behaves as if
hosted and executes nothing — the safe default, so a forgotten setting can never
be the unsafe outcome.

The sidebar shows which mode you are in. Read it before trusting an output block.

---

## Deploy to Streamlit Community Cloud

### 1. Check two things first

**Can you keep it private?** By default a Community Cloud app URL works for
anyone who has it, and your OpenRouter key sits behind it — so a public link is
also a billing exposure. Community Cloud can deploy from a **private** GitHub
repo and restrict viewers to named email addresses. Confirm what your account
allows before you push, because `corpus/` and `baseline.md` go into that repo.

**Is `style-guide.md` committed?** The app refuses to generate without it. Build
it locally first, read it, correct it, then commit it:

```
python -m tr --curriculum curricula/genai-2026.yaml style --from-curriculum --limit 16
```

### 2. Push to GitHub

```
git init
git add .
git commit -m "TR doc generator"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

`.gitignore` already excludes `work/`, `out/`, `.cache/` and `.env`. That matters
a lot here: `.cache/` currently holds the 93 downloaded decks at **1.8 GB** —
past GitHub's limits, and it would make every clone painful. The app re-downloads
decks from the Slides URLs on demand, so none of it needs committing. Without the
cache the repo is about **1 MB**.

### 3. Create the app

At <https://share.streamlit.io> → **New app**:

- Repository: `<you>/<repo>`
- Branch: `main`
- Main file path: `app.py`

### 4. Add the key

App → **Settings → Secrets**:

```toml
OPENROUTER_API_KEY = "sk-or-..."
```

Saving restarts the app. Do **not** set `TR_LOCAL` here — that would turn on code
execution on Streamlit's servers, which is exactly what you do not want.

### 5. Redeploys

Every `git push` to `main` redeploys automatically. Editing a prompt in
`prompts/` and pushing is enough to change how docs are written — no code change.

---

## What must be in the repo for the app to work

| Path | Why |
|---|---|
| `app.py`, `tr/`, `prompts/` | the app and the engine |
| `requirements.txt` | Streamlit installs from this |
| `config.yaml`, `sources.yaml` | model slugs, trusted domains |
| `curricula/*.yaml` | the course dropdown reads these |
| `baseline.md` | student knowledge baseline, injected into every run |
| `style-guide.md` | required; the app refuses without it |
| `corpus/tr_docs/**` | previous/next session docs, quoted verbatim |

Deck URLs live inside the curricula, so `corpus/ppts/` can stay empty.

---

## Things that will bite you

**Slow first run per deck.** A session whose previous session has no TR doc falls
back to its slide deck, which the app downloads on demand — a few seconds. Cloud
storage is ephemeral, so this repeats after the app sleeps.

**Community Cloud apps sleep** when idle and take ~30s to wake.

**Two people, one topic.** Output is downloaded, not written to the repo, so
concurrent users do not overwrite each other's docs. But they do share your
OpenRouter budget.

**A long generation can hit the request timeout.** The writer call on a big
session with two neighbour docs plus a deck is a large prompt. If it times out,
narrow the inputs or use a faster model slug in `config.yaml`.

**`config.yaml`'s `execute_snippets` does not control the app.** The CLI reads
it; the app decides from `TR_LOCAL` alone. That split is deliberate — a config
file committed to a public repo must not be able to switch on code execution in a
hosted deployment.
