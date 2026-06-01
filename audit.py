import requests
import re
import time
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
MONEY_RE = re.compile(r'£\s*\d+(?:[,.]?\d+)*')

URLS = [
    "https://www.freebets.com/betting-sites/reviews/bet442-sports/",
    "https://www.freebets.com/betting-sites/reviews/betduel-sports/",
    "https://www.freebets.com/betting-sites/reviews/betzone-sports/",
    "https://www.freebets.com/betting-sites/reviews/fafabet-sports/",
    "https://www.freebets.com/betting-sites/reviews/lucky-mate-sports/",
    "https://www.freebets.com/betting-sites/reviews/ruby-bet-sports/",
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
    "https://www.freebets.com/betting-sites/reviews/neptune-play-sports/",
    "https://www.freebets.com/betting-sites/reviews/quick-bet-sports/",
    "https://www.freebets.com/betting-sites/reviews/midnite-sports/",
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
]

def brand_from_url(url):
    slug = url.rstrip('/').split('/')[-1]
    slug = re.sub(r'-sports$|-sport$|-sportsbook$', '', slug)
    return slug.replace('-', ' ').title()

def extract(url):
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # CTA offer text
    cta_el = soup.select_one('.featured-offer__bonus')
    cta_text = cta_el.get_text(separator=' ', strip=True) if cta_el else None

    # Monetary amounts in article body paragraphs
    # Try common article containers
    article = (
        soup.select_one('article') or
        soup.select_one('.entry-content') or
        soup.select_one('.post-content') or
        soup.select_one('main')
    )
    amounts = []
    if article:
        for p in article.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4']):
            amounts.extend(MONEY_RE.findall(p.get_text()))
    amounts = list(dict.fromkeys(amounts))  # dedupe, preserve order

    return cta_text, amounts

results = []
for i, url in enumerate(URLS):
    brand = brand_from_url(url)
    print(f"[{i+1}/{len(URLS)}] {brand} ...", flush=True)
    try:
        cta, amounts = extract(url)
        results.append((brand, url, cta, amounts))
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append((brand, url, None, []))
    if i < len(URLS) - 1:
        time.sleep(0.5)

# Categorise
needs_amending = []   # CTA present, but CTA amounts not found in article body
no_offer = []         # CTA box missing
evergreen = []        # No CTA, no monetary amounts in article
clean = []            # CTA present and amounts match / article has no amounts

def extract_amounts_from_text(text):
    return MONEY_RE.findall(text) if text else []

for brand, url, cta, body_amounts in results:
    if cta is None:
        # No CTA box
        if not body_amounts:
            evergreen.append(brand)
        else:
            no_offer.append(brand)
    else:
        cta_amounts = extract_amounts_from_text(cta)
        if not body_amounts:
            # Evergreen article with a CTA — treat as clean
            clean.append((brand, cta, body_amounts))
        elif cta_amounts and not any(a in body_amounts for a in cta_amounts):
            needs_amending.append((brand, cta, body_amounts))
        else:
            clean.append((brand, cta, body_amounts))

print("\n=== RESULTS ===")
print(f"Needs amending ({len(needs_amending)}):")
for b, c, a in needs_amending:
    print(f"  {b} | CTA: {c} | Article: {', '.join(a[:5])}")

print(f"\nNo active offer ({len(no_offer)}):")
for b in no_offer:
    print(f"  {b}")

print(f"\nEvergreen ({len(evergreen)}):")
for b in evergreen:
    print(f"  {b}")

print(f"\nClean ({len(clean)}):")
for item in clean:
    print(f"  {item[0]}")
