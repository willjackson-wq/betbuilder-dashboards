#!/usr/bin/env python3
"""
Daily card betting tips generator.
Runs via GitHub Actions — no interactive session, no timeouts.

Required secrets (set in GitHub repo settings):
  ANTHROPIC_API_KEY  — Anthropic API key
  SLACK_BOT_TOKEN    — Slack bot token (optional)
  SERPER_API_KEY     — Serper.dev search API key (optional but recommended)

GITHUB_TOKEN is provided automatically by GitHub Actions.
"""

import os
import sys
import json
import base64
import datetime
import requests
import anthropic

# ── Config ───────────────────────────────────────────────────────────────────
REPO_OWNER       = "willjackson-wq"
REPO_NAME        = "betbuilder-dashboards"
FILE_PATH        = "card-betting-tips.html"
DASHBOARD_BRANCH = "dashboard"
SLACK_CHANNEL    = "#fb-page-updates"
DASHBOARD_URL    = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/{FILE_PATH}"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_TOKEN      = os.environ.get("GITHUB_TOKEN", "")
SLACK_TOKEN       = os.environ.get("SLACK_BOT_TOKEN", "")
SERPER_API_KEY    = os.environ.get("SERPER_API_KEY", "")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(SCRIPT_DIR)


# ── Web search ────────────────────────────────────────────────────────────────
def search(query: str) -> str:
    """Search via Serper.dev. Returns snippet text or empty string."""
    if not SERPER_API_KEY:
        return ""
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": 5},
            timeout=15,
        )
        results = r.json().get("organic", [])
        return "\n".join(f"{i.get('title','')}: {i.get('snippet','')}" for i in results[:5])
    except Exception as e:
        print(f"[search] warning: {e}")
        return ""


# ── Generate tips via Claude API ──────────────────────────────────────────────
def generate_tips() -> dict:
    today     = datetime.date.today()
    tomorrow  = today + datetime.timedelta(days=1)
    day_after = today + datetime.timedelta(days=2)

    today_str     = today.strftime("%A %d %B %Y")
    tomorrow_str  = tomorrow.strftime("%A %d %B %Y")
    day_after_str = day_after.strftime("%A %d %B %Y")

    # Gather search context (best-effort)
    searches = [
        f"UEFA Champions League Europa League fixtures {today_str}",
        f"UEFA Champions League Europa League fixtures {tomorrow_str}",
        f"Premier League fixtures {day_after_str}",
    ]
    context_parts = []
    for q in searches:
        result = search(q)
        if result:
            context_parts.append(f"Query: {q}\n{result}")

    search_context = (
        "\n\n".join(context_parts)
        if context_parts
        else "No search results — use your training knowledge for upcoming fixtures."
    )

    prompt = f"""You are a professional football betting analyst specialising in yellow card markets.
Today is {today_str}.

SEARCH CONTEXT (may be partial):
{search_context}

TASK
Generate yellow card / player-to-be-carded betting tips for:
  TODAY          — {today_str}
  TOMORROW       — {tomorrow_str}
  DAY AFTER      — {day_after_str}

COMPETITIONS (in priority order):
  UEFA Champions League, UEFA Europa League, Premier League (midweek only)

TARGET PROFILE:
  • Combative CDM/CM with high season foul rate
  • Player on booking tightrope (4+ yellows)
  • Team chasing aggregate deficit (desperate tackle rate rises)
  • Referee averaging >3.5 cards/game

RULES:
  • Aim for 1–3 tips per day where fixtures exist; empty array if no fixtures
  • kickOff must be 24-hour UK time (BST = UTC+1 in April)
  • boyleSportsOdds must be fractional (e.g. 6/4, 5/2, 13/8)
  • foulsPerGame: use null if unverifiable
  • analysisP1: exactly two sentences about the player's stats and style
  • analysisP2: exactly two sentences about match context and why a booking is likely

Return ONLY valid JSON — no markdown fences, no commentary.

SCHEMA:
{{
  "today": [
    {{
      "match": "Home Team vs Away Team",
      "league": "UEFA Europa League",
      "kickOff": "20:00",
      "context": "UEL QF 2nd leg — Home lead 2-1 on agg",
      "playerName": "First Last",
      "club": "Club Name",
      "position": "CDM",
      "tipType": "To Be Carded",
      "confidence": "HIGH",
      "boyleSportsOdds": "6/4",
      "boyleSportsUrl": "https://www.boylesports.com/sports/football/bet-builder",
      "stats": {{
        "yellowsThisSeason": 5,
        "foulsPerGame": 1.67,
        "cardsPer90": 0.32,
        "appearances": 24
      }},
      "referee": {{
        "name": "Referee Name",
        "avgCardsPerGame": 3.63
      }},
      "analysisP1": "Sentence one. Sentence two.",
      "analysisP2": "Sentence one. Sentence two."
    }}
  ],
  "tomorrow": [],
  "dayAfterTomorrow": []
}}"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip accidental markdown fences
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


# ── Build HTML from template ──────────────────────────────────────────────────
def build_html(tips: dict) -> str:
    today     = datetime.date.today()
    tomorrow  = today + datetime.timedelta(days=1)
    day_after = today + datetime.timedelta(days=2)

    generated_date = (
        today.strftime("%a %d %b %Y")
        + ", "
        + datetime.datetime.utcnow().strftime("%H:%M")
        + " UTC"
    )

    template_path = os.path.join(SCRIPT_DIR, "tips_template.html")
    with open(template_path, encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{GENERATED_DATE}}", generated_date)
    html = html.replace("{{TODAY_LABEL}}",      today.strftime("%A %d %B %Y"))
    html = html.replace("{{TOMORROW_LABEL}}",   tomorrow.strftime("%A %d %B %Y"))
    html = html.replace("{{DAY_AFTER_LABEL}}",  day_after.strftime("%A %d %B %Y"))
    html = html.replace("{{TIPS_JSON}}",        json.dumps(tips, ensure_ascii=False, indent=2))

    return html


# ── Deploy to GitHub dashboard branch ────────────────────────────────────────
def deploy_to_github(html: str):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Get existing file SHA (required for updates)
    r = requests.get(url, headers=headers, params={"ref": DASHBOARD_BRANCH})
    sha = r.json().get("sha") if r.status_code == 200 else None

    today = datetime.date.today()
    payload = {
        "message": f"Daily card betting tips update - {today.strftime('%a %d %b %Y')}",
        "content": base64.b64encode(html.encode("utf-8")).decode("ascii"),
        "branch": DASHBOARD_BRANCH,
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(url, headers=headers, json=payload)
    r.raise_for_status()
    print(f"[github] deployed: HTTP {r.status_code}")


# ── Slack notification ────────────────────────────────────────────────────────
def notify_slack(tips: dict):
    if not SLACK_TOKEN:
        print("[slack] no SLACK_BOT_TOKEN — skipping")
        return

    today    = datetime.date.today()
    date_str = today.strftime("%a %d %b")

    lines = []
    for tip in tips.get("today", []):
        parts    = tip["match"].split(" vs ")
        opponent = parts[1] if len(parts) > 1 else tip["match"]
        lines.append(f"- {tip['playerName']} ({tip['club']}) vs {opponent} — {tip['confidence']}")

    today_text = "\n".join(lines) if lines else "- No tips for today"

    text = f"Card Betting Tips — {date_str}\n\nTODAY\n{today_text}\n{DASHBOARD_URL}"

    r = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_TOKEN}",
            "Content-Type": "application/json",
        },
        json={"channel": SLACK_CHANNEL, "text": text},
        timeout=15,
    )
    data = r.json()
    if data.get("ok"):
        print("[slack] notification sent")
    else:
        print(f"[slack] error: {data.get('error')}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN not set")
        sys.exit(1)

    print("Generating tips via Claude API...")
    tips = generate_tips()
    counts = (
        len(tips.get("today", [])),
        len(tips.get("tomorrow", [])),
        len(tips.get("dayAfterTomorrow", [])),
    )
    print(f"Tips: {counts[0]} today / {counts[1]} tomorrow / {counts[2]} day-after")

    print("Building HTML from template...")
    html = build_html(tips)

    # Write locally (for git commit in workflow)
    output = os.path.join(REPO_ROOT, FILE_PATH)
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {output}")

    print("Deploying to GitHub dashboard branch...")
    deploy_to_github(html)

    print("Sending Slack notification...")
    notify_slack(tips)

    print("Done.")


if __name__ == "__main__":
    main()
