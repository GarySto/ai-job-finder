"""Weekly job search: reads your rubric and CV, asks Claude to search the web for
new roles, scores them against your rubric and saves a dated report.

Run by .github/workflows/weekly-search.yml, or locally with:
    ANTHROPIC_API_KEY=sk-... python scripts/weekly_search.py
"""

import csv
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUBRIC = ROOT / "my-search" / "rubric.md"
CV = ROOT / "my-search" / "cv.md"
SEEN = ROOT / "my-search" / "seen.csv"
RESULTS = ROOT / "results"

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
MAX_SEARCHES = int(os.environ.get("MAX_SEARCHES", "15"))
DAYS_BACK = int(os.environ.get("DAYS_BACK", "7"))
SHOW_FROM = int(os.environ.get("SHOW_FROM", "60"))

FIELDS = ["date_found", "score", "verdict", "job_title", "company",
          "location", "salary", "link", "reason", "status"]


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def load_inputs():
    rubric = RUBRIC.read_text(encoding="utf-8")
    cv = CV.read_text(encoding="utf-8")
    if "[Paste your CV here]" in cv or len(cv.strip()) < 300:
        fail("my-search/cv.md still has the placeholder text. Paste your CV in (without contact details) and run again.")
    if "Delete the example when you're done" in rubric:
        fail("my-search/rubric.md still has the example rubric. Replace it with your own and run again.")
    seen = []
    if SEEN.exists():
        with SEEN.open(newline="", encoding="utf-8") as f:
            seen = list(csv.DictReader(f))
    return rubric, cv, seen


def build_prompt(rubric, cv, seen, today):
    seen_lines = "\n".join(
        f"- {r.get('job_title', '')} at {r.get('company', '')} ({r.get('link', '')})" for r in seen
    ) or "- none yet"
    return f"""Today is {today}. You are my job search assistant.

Search the web for roles posted in the last {DAYS_BACK} days that match my rubric below.
Search job boards, company career pages and LinkedIn job listings. Aim for up to 15 new roles.

Rules:
- Only include roles you actually found in your search results, with the direct link to the advert. Never invent or guess a role, a salary or a link.
- Put the current month and year in your searches. Old adverts stay online for months.
- Check each advert's posted or closing date. Leave out anything posted more than {DAYS_BACK} days ago or already closed. If no date is shown, set date_posted to "not shown".
- Leave out any role in my "already seen" list.
- Score each role out of 100 against my rubric. Any role that hits a deal-breaker scores 0.
- Verdict: "Apply" for 75+, "Stretch" for 60-74, "Skip" below 60.
- If you can't find many good matches, return fewer. An honest short list is better than a padded one.

When you have finished searching, reply with ONLY a JSON array inside a ```json code block, nothing else. Each item:
{{"score": 0-100, "verdict": "Apply|Stretch|Skip", "job_title": "", "company": "", "location": "", "salary": "", "date_posted": "", "link": "", "reason": "one line"}}
Use "" for anything you don't know.

=== MY RUBRIC ===
{rubric}

=== MY CV ===
{cv}

=== ALREADY SEEN ===
{seen_lines}
"""


def ask_claude(prompt):
    try:
        import anthropic
    except ImportError:
        fail("The anthropic package isn't installed. Run: pip install -r requirements.txt")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        fail("ANTHROPIC_API_KEY isn't set. Add it under Settings > Secrets and variables > Actions.")

    client = anthropic.Anthropic()
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": MAX_SEARCHES}]
    messages = [{"role": "user", "content": prompt}]

    # Server-side web search can pause a long turn; send it back to let it carry on.
    for _ in range(5):
        resp = client.messages.create(model=MODEL, max_tokens=8000, tools=tools, messages=messages)
        if resp.stop_reason != "pause_turn":
            break
        messages = [messages[0], {"role": "assistant", "content": resp.content}]

    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def parse_roles(text):
    match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.S) or re.search(r"(\[\s*\{.*\}\s*\])", text, re.S)
    if not match:
        if re.search(r"\[\s*\]", text):
            return []
        fail("Couldn't find the list of roles in the AI's reply. Raw reply:\n" + text[:3000])
    try:
        roles = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        fail(f"The AI's list of roles wasn't valid JSON ({e}). Raw reply:\n" + text[:3000])
    clean = []
    for r in roles:
        link = str(r.get("link", "")).strip()
        if not link.startswith("http"):
            continue  # no real link = not a role we can trust
        try:
            score = max(0, min(100, int(float(r.get("score", 0)))))
        except (TypeError, ValueError):
            score = 0
        r["score"] = score
        r["link"] = link
        clean.append(r)
    return clean


TRACKING = ("utm_", "ref", "trk", "src", "source", "from", "tracking")


def norm(link):
    """Compare links without tracking junk, but keep IDs like Indeed's ?jk=123."""
    from urllib.parse import urlsplit, parse_qsl, urlencode
    p = urlsplit(link.strip().lower())
    query = sorted((k, v) for k, v in parse_qsl(p.query) if not k.startswith(TRACKING))
    return f"{p.netloc.removeprefix('www.')}{p.path.rstrip('/')}?{urlencode(query)}"


def main():
    today = dt.date.today().isoformat()
    rubric, cv, seen = load_inputs()
    roles = parse_roles(ask_claude(build_prompt(rubric, cv, seen, today)))

    seen_links = {norm(r.get("link", "")) for r in seen}
    new = [r for r in roles if norm(r["link"]) not in seen_links]
    new.sort(key=lambda r: r["score"], reverse=True)

    # Save every new role to the tracker so it's never shown twice.
    write_header = not SEEN.exists() or SEEN.stat().st_size == 0
    with SEEN.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        for r in new:
            w.writerow({"date_found": today, "score": r["score"], "verdict": r.get("verdict", ""),
                        "job_title": r.get("job_title", ""), "company": r.get("company", ""),
                        "location": r.get("location", ""), "salary": r.get("salary", ""),
                        "link": r["link"], "reason": r.get("reason", ""), "status": "New"})

    shortlist = [r for r in new if r["score"] >= SHOW_FROM]
    lines = [f"# Job sweep for {today}", "",
             f"Found **{len(new)}** new role(s). **{len(shortlist)}** scored {SHOW_FROM} or more.", ""]
    if shortlist:
        lines += ["| Score | Verdict | Job title | Company | Location | Salary | Posted | Link | Why |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for r in shortlist:
            cells = [str(r["score"]), r.get("verdict", ""), r.get("job_title", ""), r.get("company", ""),
                     r.get("location", ""), r.get("salary", ""), r.get("date_posted", ""),
                     f"[Open advert]({r['link']})", r.get("reason", "")]
            lines.append("| " + " | ".join(str(c).replace("|", "/") for c in cells) + " |")
    else:
        lines.append(f"Nothing scored {SHOW_FROM} or more this week. That's useful to know too.")
    lines += ["", "Always open the advert and check it before applying. AI can misread details.",
              "Every new role, including the low scorers, has been added to `my-search/seen.csv`."]

    RESULTS.mkdir(exist_ok=True)
    report = RESULTS / f"{today}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"report={report.relative_to(ROOT)}\nshortlist={len(shortlist)}\nnew={len(new)}\n")


if __name__ == "__main__":
    main()
