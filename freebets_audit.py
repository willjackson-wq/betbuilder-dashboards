#!/usr/bin/env python3
"""
Freebets review page audit.
Fetches all /betting-sites/reviews/ pages, checks CTA vs article body amounts,
then prints a Slack-ready report.
"""

import re
import time
import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA}
MONEY_RE = re.compile(r'£\s?\d[\d,]*(?:\.\d{1,2})?')

URLS = [
    "https://www.freebets.com/betting-sites/reviews/10bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/21-co-uk-sports/",
    "https://www.freebets.com/betting-sites/reviews/21luckybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/247bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/7bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/888-sport/",
    "https://www.freebets.com/betting-sites/reviews/all-british-casino-sports/",
    "https://www.freebets.com/betting-sites/reviews/bet365/",
    "https://www.freebets.com/betting-sites/reviews/bet442-sports/",
    "https://www.freebets.com/betting-sites/reviews/betano-sports/",
    "https://www.freebets.com/betting-sites/reviews/betdaq-sports/",
    "https://www.freebets.com/betting-sites/reviews/betduel-sports/",
    "https://www.freebets.com/betting-sites/reviews/betfair-sportsbook/",
    "https://www.freebets.com/betting-sites/reviews/betfred-sports/",
    "https://www.freebets.com/betting-sites/reviews/betgoodwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/betmaze-sports/",
    "https://www.freebets.com/betting-sites/reviews/betmgm-sports/",
    "https://www.freebets.com/betting-sites/reviews/betrino-sports/",
    "https://www.freebets.com/betting-sites/reviews/bettom-sports/",
    "https://www.freebets.com/betting-sites/reviews/betuk-sports/",
    "https://www.freebets.com/betting-sites/reviews/betvictor-sports/",
    "https://www.freebets.com/betting-sites/reviews/betway-sports/",
    "https://www.freebets.com/betting-sites/reviews/betwright-sports/",
    "https://www.freebets.com/betting-sites/reviews/betzone-sports/",
    "https://www.freebets.com/betting-sites/reviews/boylesports/",
    "https://www.freebets.com/betting-sites/reviews/bwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/casino-kings-sports/",
    "https://www.freebets.com/betting-sites/reviews/copybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/coral-sports/",
    "https://www.freebets.com/betting-sites/reviews/dafabet-sports/",
    "https://www.freebets.com/betting-sites/reviews/dream-vegas-sports/",
    "https://www.freebets.com/betting-sites/reviews/easybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/fafabet-sports/",
    "https://www.freebets.com/betting-sites/reviews/fitzdares-sport/",
    "https://www.freebets.com/betting-sites/reviews/fruity-king-sports/",
    "https://www.freebets.com/betting-sites/reviews/funky-jackpot-sports/",
    "https://www.freebets.com/betting-sites/reviews/grosvenor-sports/",
    "https://www.freebets.com/betting-sites/reviews/highbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/jeffbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/kwiff-sports/",
    "https://www.freebets.com/betting-sites/reviews/ladbrokes-sports/",
    "https://www.freebets.com/betting-sites/reviews/livescorebet-sports/",
    "https://www.freebets.com/betting-sites/reviews/lottoland-sports/",
    "https://www.freebets.com/betting-sites/reviews/lucky-mate-sports/",
    "https://www.freebets.com/betting-sites/reviews/matchbook-sports/",
    "https://www.freebets.com/betting-sites/reviews/midnite-sports/",
    "https://www.freebets.com/betting-sites/reviews/monster-sports/",
    "https://www.freebets.com/betting-sites/reviews/mrluck-sports/",
    "https://www.freebets.com/betting-sites/reviews/neptune-play-sports/",
    "https://www.freebets.com/betting-sites/reviews/netbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/paddy-power-sports/",
    "https://www.freebets.com/betting-sites/reviews/parimatch-sports/",
    "https://www.freebets.com/betting-sites/reviews/playzee/",
    "https://www.freebets.com/betting-sites/reviews/pricedup-sports/",
    "https://www.freebets.com/betting-sites/reviews/pub-sports/",
    "https://www.freebets.com/betting-sites/reviews/puntit-sports/",
    "https://www.freebets.com/betting-sites/reviews/quick-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/quinnbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/ruby-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/sbk-sports/",
    "https://www.freebets.com/betting-sites/reviews/sky-bet/",
    "https://www.freebets.com/betting-sites/reviews/smarkets-sports/",
    "https://www.freebets.com/betting-sites/reviews/spinzwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/sporting-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/sporting-index-sports/",
    "https://www.freebets.com/betting-sites/reviews/spreadex-sports/",
    "https://www.freebets.com/betting-sites/reviews/star-sports/",
    "https://www.freebets.com/betting-sites/reviews/talksport-bet/",
    "https://www.freebets.com/betting-sites/reviews/the-online-casino-sports/",
    "https://www.freebets.com/betting-sites/reviews/tote-sports/",
    "https://www.freebets.com/betting-sites/reviews/unibet-sports/",
    "https://www.freebets.com/betting-sites/reviews/vegasmobilecasino-sports/",
    "https://www.freebets.com/betting-sites/reviews/virginbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/william-hill-sports/",
]


def brand_from_url(url):
    slug = url.rstrip("/").split("/")[-1]
    slug = re.sub(r"-sports?$", "", slug)
    slug = re.sub(r"-sportsbook$", "", slug)
    return slug.replace("-", " ").title()


def audit_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # CTA offer text
    cta_el = soup.select_one(".featured-offer__bonus")
    cta_text = cta_el.get_text(" ", strip=True) if cta_el else None

    # Article body paragraphs
    article = soup.select_one("article") or soup.select_one(".entry-content") or soup.select_one("main")
    body_amounts = []
    if article:
        for p in article.find_all("p"):
            found = MONEY_RE.findall(p.get_text())
            body_amounts.extend(found)
    # Normalise: remove space after £, strip trailing punctuation, dedupe
    # Cap at £999 to ignore deposit/withdrawal limits which are always far larger
    def normalise(amt):
        return re.sub(r'£\s+', '£', amt).rstrip(',.')

    def numeric_value(amt):
        return int(re.sub(r'[£,]', '', amt))

    body_amounts = list(dict.fromkeys(
        normalise(a) for a in body_amounts if numeric_value(a) <= 999
    ))

    return cta_text, body_amounts


def main():
    needs_amending = []    # CTA present, CTA amounts not in article
    no_offer = []          # CTA missing
    evergreen = []         # No monetary amounts in article at all
    clean = []             # Everything lines up

    total = len(URLS)
    for i, url in enumerate(URLS, 1):
        brand = brand_from_url(url)
        print(f"[{i}/{total}] {brand} ...", flush=True)
        try:
            cta_text, body_amounts = audit_page(url)
        except Exception as e:
            print(f"  ERROR: {e}")
            no_offer.append(brand)
            time.sleep(0.5)
            continue

        if cta_text is None:
            no_offer.append(brand)
        elif not body_amounts:
            evergreen.append(brand)
        else:
            # Check if any amounts from the CTA appear in the body
            def normalise(amt):
                return re.sub(r'£\s+', '£', amt).rstrip(',.')

            cta_amounts = [normalise(a) for a in MONEY_RE.findall(cta_text)]
            matched = any(a in body_amounts for a in cta_amounts)
            if cta_amounts and not matched:
                needs_amending.append((brand, cta_text, body_amounts))
            else:
                clean.append(brand)

        time.sleep(0.5)

    # Build report
    from datetime import date
    today = date.today().strftime("%A %-d %B %Y")

    lines = [
        f"*Freebets Reviews Audit — {today}*",
        f"Checked {total} pages under freebets.com/betting-sites/reviews/",
        "",
    ]

    if needs_amending:
        lines.append("*Pages where CTA doesn't match article (needs amending):*")
        for brand, cta, amounts in needs_amending:
            lines.append(f"• {brand} — CTA: {cta} | Article mentions: {', '.join(amounts)}")
        lines.append("")

    if no_offer:
        lines.append("*No active offer (monitor for return):*")
        for brand in no_offer:
            lines.append(f"• {brand}")
        lines.append("")

    n_clean = len(clean) + len(evergreen)
    lines.append(f"Clean run for remaining {n_clean} pages — no action required.")

    report = "\n".join(lines)
    print("\n--- SLACK REPORT ---")
    print(report)
    print("--- END REPORT ---\n")

    # Save to file for posting
    with open("/tmp/freebets_report.txt", "w") as f:
        f.write(report)

    return report


if __name__ == "__main__":
    main()
