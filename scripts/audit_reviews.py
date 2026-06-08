#!/usr/bin/env python3
"""
Freebets betting-sites/reviews audit script.
"""
import re
import time
import json
import urllib.request

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

URLS = [
    "https://www.freebets.com/betting-sites/reviews/bet442-sports/",
    "https://www.freebets.com/betting-sites/reviews/betduel-sports/",
    "https://www.freebets.com/betting-sites/reviews/betzone-sports/",
    "https://www.freebets.com/betting-sites/reviews/fafabet-sports/",
    "https://www.freebets.com/betting-sites/reviews/lucky-mate-sports/",
    "https://www.freebets.com/betting-sites/reviews/parimatch-sports/",
    "https://www.freebets.com/betting-sites/reviews/spinzwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/matchbook-sports/",
    "https://www.freebets.com/betting-sites/reviews/highbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/smarkets-sports/",
    "https://www.freebets.com/betting-sites/reviews/10bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/grosvenor-sports/",
    "https://www.freebets.com/betting-sites/reviews/lottoland-sports/",
    "https://www.freebets.com/betting-sites/reviews/jeffbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/betdaq-sports/",
    "https://www.freebets.com/betting-sites/reviews/sbk-sports/",
    "https://www.freebets.com/betting-sites/reviews/sporting-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/888-sport/",
    "https://www.freebets.com/betting-sites/reviews/virginbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/21luckybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/casino-kings-sports/",
    "https://www.freebets.com/betting-sites/reviews/fruity-king-sports/",
    "https://www.freebets.com/betting-sites/reviews/betmgm-sports/",
    "https://www.freebets.com/betting-sites/reviews/sporting-index-sports/",
    "https://www.freebets.com/betting-sites/reviews/unibet-sports/",
    "https://www.freebets.com/betting-sites/reviews/pub-sports/",
    "https://www.freebets.com/betting-sites/reviews/quick-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/mrluck-sports/",
    "https://www.freebets.com/betting-sites/reviews/talksport-bet/",
    "https://www.freebets.com/betting-sites/reviews/copybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/tote-sports/",
    "https://www.freebets.com/betting-sites/reviews/playzee/",
    "https://www.freebets.com/betting-sites/reviews/betgoodwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/betuk-sports/",
    "https://www.freebets.com/betting-sites/reviews/star-sports/",
    "https://www.freebets.com/betting-sites/reviews/the-online-casino-sports/",
    "https://www.freebets.com/betting-sites/reviews/pricedup-sports/",
    "https://www.freebets.com/betting-sites/reviews/vegasmobilecasino-sports/",
    "https://www.freebets.com/betting-sites/reviews/betrino-sports/",
    "https://www.freebets.com/betting-sites/reviews/bwin-sports/",
    "https://www.freebets.com/betting-sites/reviews/coral-sports/",
    "https://www.freebets.com/betting-sites/reviews/paddy-power-sports/",
    "https://www.freebets.com/betting-sites/reviews/betfair-sportsbook/",
    "https://www.freebets.com/betting-sites/reviews/bet365/",
    "https://www.freebets.com/betting-sites/reviews/all-british-casino-sports/",
    "https://www.freebets.com/betting-sites/reviews/betfred-sports/",
    "https://www.freebets.com/betting-sites/reviews/bettom-sports/",
    "https://www.freebets.com/betting-sites/reviews/247bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/7bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/betmaze-sports/",
    "https://www.freebets.com/betting-sites/reviews/boylesports/",
    "https://www.freebets.com/betting-sites/reviews/funky-jackpot-sports/",
    "https://www.freebets.com/betting-sites/reviews/kwiff-sports/",
    "https://www.freebets.com/betting-sites/reviews/quinnbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/betano-sports/",
    "https://www.freebets.com/betting-sites/reviews/betvictor-sports/",
    "https://www.freebets.com/betting-sites/reviews/easybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/ladbrokes-sports/",
    "https://www.freebets.com/betting-sites/reviews/livescorebet-sports/",
    "https://www.freebets.com/betting-sites/reviews/monster-sports/",
    "https://www.freebets.com/betting-sites/reviews/puntit-sports/",
    "https://www.freebets.com/betting-sites/reviews/21-co-uk-sports/",
    "https://www.freebets.com/betting-sites/reviews/dafabet-sports/",
    "https://www.freebets.com/betting-sites/reviews/william-hill-sports/",
    "https://www.freebets.com/betting-sites/reviews/sky-bet/",
    "https://www.freebets.com/betting-sites/reviews/betway-sports/",
    "https://www.freebets.com/betting-sites/reviews/betwright-sports/",
    "https://www.freebets.com/betting-sites/reviews/fitzdares-sport/",
    "https://www.freebets.com/betting-sites/reviews/spreadex-sports/",
    "https://www.freebets.com/betting-sites/reviews/dream-vegas-sports/",
    "https://www.freebets.com/betting-sites/reviews/netbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/neptune-play-sports/",
    "https://www.freebets.com/betting-sites/reviews/ruby-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/midnite-sports/",
]

MONEY_RE = re.compile(r'£\d+(?:,\d{3})*(?:\.\d+)?')
STRIP_TAGS = re.compile(r'<[^>]+>')


def brand_from_url(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    slug = slug.replace("-sports", "").replace("-sport", "")
    return slug.replace("-", " ").title()


def fetch(url: str) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None


def strip_tags(s: str) -> str:
    return STRIP_TAGS.sub(" ", s).strip()


def extract_bonus(html: str) -> str | None:
    """Extract text from the featured-offer__bonus div (first occurrence)."""
    m = re.search(
        r'class="[^"]*featured-offer__bonus[^"]*"[^>]*>(.*?)</div',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None
    text = strip_tags(m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    return text or None


def remove_cta_block(html: str) -> str:
    """Strip the entire featured-offer block so its £ amounts don't bleed into body."""
    # Remove all elements with class containing "featured-offer"
    cleaned = re.sub(
        r'<(?:div|section|aside)[^>]*class="[^"]*featured-offer[^"]*"[^>]*>.*?</(?:div|section|aside)>',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return cleaned


def extract_body_amounts(html: str) -> list[str]:
    """Extract unique monetary amounts from <p> tags in the article body."""
    # Remove CTA/widget blocks first
    body = remove_cta_block(html)

    # Collect text from all <p> tags
    paras = re.findall(r'<p[^>]*>(.*?)</p>', body, re.DOTALL | re.IGNORECASE)
    combined = ' '.join(strip_tags(p) for p in paras)

    amounts = MONEY_RE.findall(combined)
    # Normalise: remove internal spaces, deduplicate preserving order
    seen = set()
    result = []
    for a in amounts:
        a = re.sub(r'\s+', '', a)  # £ 10 -> £10
        if a not in seen:
            seen.add(a)
            result.append(a)
    return result


def main():
    needs_amending = []
    no_offer = []
    evergreen = []
    clean = []

    total = len(URLS)
    print(f"Processing {total} URLs...\n")

    for i, url in enumerate(URLS, 1):
        brand = brand_from_url(url)
        print(f"[{i:02d}/{total}] {brand}", end=" ... ", flush=True)
        html = fetch(url)
        if html is None:
            print("SKIP (fetch error)")
            no_offer.append(brand)
            time.sleep(0.5)
            continue

        bonus = extract_bonus(html)
        amounts = extract_body_amounts(html)

        if bonus is None:
            print("no CTA")
            no_offer.append(brand)
        elif not amounts:
            # No monetary amounts anywhere in the article body
            print(f"evergreen | CTA: {bonus[:80]!r}…")
            evergreen.append((brand, bonus))
        else:
            # Check whether CTA headline amounts appear in article body
            cta_amounts = list(dict.fromkeys(
                re.sub(r'\s+', '', a) for a in MONEY_RE.findall(bonus)
            ))
            missing = [a for a in cta_amounts if a not in amounts]
            if cta_amounts and missing:
                print(f"NEEDS AMENDING | CTA amounts {cta_amounts} | article: {amounts}")
                needs_amending.append((brand, bonus, amounts))
            else:
                print(f"clean | CTA: {bonus[:60]!r}…")
                clean.append(brand)

        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nNeeds amending ({len(needs_amending)}):")
    for brand, cta, amounts in needs_amending:
        # Extract just the headline from CTA (first sentence before T&C boilerplate)
        headline = cta.split("Claim Offer")[0].strip()
        print(f"  {brand} — CTA: {headline!r} | Article mentions: {', '.join(amounts)}")

    print(f"\nNo active offer ({len(no_offer)}):")
    for b in no_offer:
        print(f"  {b}")

    print(f"\nEvergreen / no monetary amounts in body ({len(evergreen)}):")
    for brand, cta in evergreen:
        headline = cta.split("Claim Offer")[0].strip()
        print(f"  {brand} — CTA: {headline!r}")

    print(f"\nClean ({len(clean)}):")
    for b in clean:
        print(f"  {b}")

    result = {
        "total": total,
        "needs_amending": [
            {
                "brand": b,
                "cta_headline": c.split("Claim Offer")[0].strip(),
                "amounts": a,
            }
            for b, c, a in needs_amending
        ],
        "no_offer": no_offer,
        "evergreen": [
            {"brand": b, "cta_headline": c.split("Claim Offer")[0].strip()}
            for b, c in evergreen
        ],
        "clean": clean,
    }
    with open("/tmp/audit_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\nWrote /tmp/audit_result.json")


if __name__ == "__main__":
    main()
