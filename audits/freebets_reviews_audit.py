#!/usr/bin/env python3
"""
Freebets /betting-sites/reviews/ audit.

Fetches all review URLs from the live sitemap, checks each page for:
  - A featured-offer__bonus CTA box
  - Whether the CTA's monetary amounts appear in the article body

Posts results to Slack channel #fb-page-updates.

Required env var: SLACK_BOT_TOKEN
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error
import json
from datetime import date

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SITEMAP_URL = "https://www.freebets.com/sitemap.xml"
REVIEWS_PREFIX = "https://www.freebets.com/betting-sites/reviews/"
SLACK_CHANNEL = "C0ANL746CB1"
REQUEST_DELAY = 0.5  # seconds between page fetches

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Sitemap
# ---------------------------------------------------------------------------

def get_review_urls() -> list[str]:
    """Return all /betting-sites/reviews/<slug>/ URLs from the sitemap, excluding the index."""
    xml = fetch(SITEMAP_URL)
    urls = re.findall(r'<loc>(https?://[^<]+)</loc>', xml)
    return [
        u for u in urls
        if u.startswith(REVIEWS_PREFIX) and u.rstrip("/") != REVIEWS_PREFIX.rstrip("/")
    ]


# ---------------------------------------------------------------------------
# Page parsing
# ---------------------------------------------------------------------------

def extract_cta(html: str) -> str | None:
    """Return text inside featured-offer__bonus, or None if the element is absent."""
    m = re.search(r'class="featured-offer__bonus[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if not m:
        return None
    text = re.sub(r'<[^>]+>', '', m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    return text or None


def extract_article_amounts(html: str) -> list[str]:
    """Return unique GBP amounts found in article body paragraphs."""
    # Strip scripts and styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    article = ''
    for pattern in (
        r'class="entry-content[^"]*"[^>]*>(.*?)</article',
        r'<article[^>]*>(.*?)</article',
    ):
        m = re.search(pattern, html, re.DOTALL)
        if m:
            article = m.group(1)
            break

    if not article:
        # Fallback: everything after the CTA block
        idx = html.find('featured-offer__bonus')
        article = html[idx:] if idx >= 0 else html

    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', article, re.DOTALL)
    text = ' '.join(re.sub(r'<[^>]+>', '', p) for p in paragraphs)
    amounts = re.findall(r'£\d+(?:,\d{3})*(?:\.\d+)?', text)
    return list(dict.fromkeys(amounts))  # dedupe, preserve order


def cta_amounts(cta_text: str) -> list[str]:
    return re.findall(r'£\d+(?:,\d{3})*(?:\.\d+)?', cta_text)


# ---------------------------------------------------------------------------
# Categorisation
# ---------------------------------------------------------------------------

def categorise(pages: list[dict]) -> tuple[list, list, list]:
    needs_amending, no_offer, clean = [], [], []
    for p in pages:
        cta, amounts = p["cta"], p["amounts"]
        if cta is None:
            no_offer.append(p)
        elif not amounts:
            # No monetary amounts in article = evergreen page
            clean.append(p)
        else:
            missing = [a for a in cta_amounts(cta) if a not in amounts]
            (needs_amending if missing else clean).append(p)
    return needs_amending, no_offer, clean


# ---------------------------------------------------------------------------
# Slack
# ---------------------------------------------------------------------------

def post_slack(message: str) -> None:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print("SLACK_BOT_TOKEN not set — printing report instead:\n")
        print(message)
        return

    payload = json.dumps({
        "channel": SLACK_CHANNEL,
        "text": message,
    }).encode()

    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read())
    if not body.get("ok"):
        raise RuntimeError(f"Slack error: {body.get('error')}")


def build_message(needs_amending, no_offer, clean, total) -> str:
    today = date.today()
    day_name = today.strftime("%A")
    date_str = today.strftime("%-d %B %Y")

    lines = [
        f"*Freebets Reviews Audit — {day_name} {date_str}*",
        f"Checked {total} pages under freebets.com/betting-sites/reviews/",
        "",
        "---",
        "",
    ]

    lines.append("*Pages where CTA doesn't match article (needs amending):*")
    if needs_amending:
        for p in needs_amending:
            amounts_str = ', '.join(p['amounts'])
            lines.append(f"• {p['brand']} — CTA: {p['cta']} | Article mentions: {amounts_str}")
    else:
        lines.append("None")

    lines += ["", "---", ""]

    lines.append("*No active offer (monitor for return):*")
    if no_offer:
        lines.append(', '.join(p['brand'] for p in no_offer))
    else:
        lines.append("None")

    lines += ["", "---", ""]

    lines.append(f"Clean run for remaining {len(clean)} pages — no action required.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Fetching review URLs from sitemap...", flush=True)
    urls = get_review_urls()
    if not urls:
        print("ERROR: No review URLs found in sitemap. Aborting.")
        sys.exit(1)
    print(f"Found {len(urls)} review pages.", flush=True)

    pages = []
    for i, url in enumerate(urls, 1):
        brand = url.rstrip("/").split("/")[-1]
        print(f"[{i}/{len(urls)}] {brand}", flush=True)
        try:
            html = fetch(url)
        except urllib.error.URLError as exc:
            print(f"  WARN: fetch failed ({exc}), skipping")
            continue
        pages.append({
            "brand": brand,
            "url": url,
            "cta": extract_cta(html),
            "amounts": extract_article_amounts(html),
        })
        if i < len(urls):
            time.sleep(REQUEST_DELAY)

    needs_amending, no_offer, clean = categorise(pages)

    print(f"\nNeeds amending: {len(needs_amending)}")
    print(f"No offer / monitor: {len(no_offer)}")
    print(f"Clean: {len(clean)}")

    message = build_message(needs_amending, no_offer, clean, len(pages))
    post_slack(message)
    print("\nDone.")


if __name__ == "__main__":
    main()
