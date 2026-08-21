"""Gather sources for a session topic and tag each one trusted or unvetted."""
import re
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s\)\]\>\"']+")

RESEARCH_PROMPT = """Research the topic below so a course author can teach it \
accurately today. Search the web -- do not answer from memory.

Topic: {topic}
Course: {course}
The learner already covered: {previous}
{next_line}

Report, with a source URL on every factual line:

## Current state
The library/API/model names and their CURRENT version numbers as of now.
Flag anything that changed or was deprecated in the last 12 months.

## Canonical minimal example
The smallest correct code example from official documentation. Say which page.

## Common failure modes
Real errors people hit, and the cause. Cite where each is documented.

## Non-obvious design decisions
Where a builder must choose between two approaches, and what the official
guidance says. These become the doc's judgment-teaching sections.

## Do not confuse with
Terms or APIs that are commonly mixed up with this topic.

Every claim needs a URL. If you cannot find a source for something, say
"no source found" rather than stating it anyway."""


def domain_of(url):
    try:
        return (urlparse(url).hostname or "").lower().lstrip("www.")
    except ValueError:
        return ""


def is_trusted(url, trusted):
    host = domain_of(url)
    return any(host == d or host.endswith("." + d) for d in trusted)


def extract_urls(message):
    """URLs from OpenRouter annotations, falling back to the text body."""
    urls = []
    for ann in getattr(message, "annotations", None) or []:
        cite = None
        if isinstance(ann, dict):
            cite = ann.get("url_citation") or ann
        else:
            cite = getattr(ann, "url_citation", None)
        url = (cite or {}).get("url") if isinstance(cite, dict) else getattr(cite, "url", None)
        if url:
            urls.append(url)
    urls += URL_RE.findall(message.content or "")
    seen, out = set(), []
    for u in urls:
        u = u.rstrip(".,;")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def research(client, model, topic, course, previous, next_title, trusted):
    """Return (markdown_notes, [(url, trusted_bool)])."""
    next_line = f"The next session covers: {next_title}" if next_title else ""
    prompt = RESEARCH_PROMPT.format(
        topic=topic, course=course, previous=previous, next_line=next_line
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        extra_body={"plugins": [{"id": "web", "max_results": 8}]},
    )
    msg = resp.choices[0].message
    urls = [(u, is_trusted(u, trusted)) for u in extract_urls(msg)]
    return msg.content or "", urls


def render_notes(topic, notes, urls):
    lines = [f"# Research: {topic}", "", notes, "", "## Sources", ""]
    if not urls:
        lines.append("No URLs returned. Research pass found nothing citable -- "
                     "the doc will be written with `[NEEDS: source]` markers.")
    for url, ok in urls:
        tag = "trusted" if ok else "unvetted"
        lines.append(f"- [{tag}] {url}")
    return "\n".join(lines)
