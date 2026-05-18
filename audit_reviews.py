#!/usr/bin/env python3
import urllib.request
import urllib.error
import time
import re
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

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
    "https://www.freebets.com/betting-sites/reviews/netbet-sports/",
    "https://www.freebets.com/betting-sites/reviews/21luckybet-sports/",
    "https://www.freebets.com/betting-sites/reviews/casino-kings-sports/",
    "https://www.freebets.com/betting-sites/reviews/fruity-king-sports/",
    "https://www.freebets.com/betting-sites/reviews/spreadex-sports/",
    "https://www.freebets.com/betting-sites/reviews/betmgm-sports/",
    "https://www.freebets.com/betting-sites/reviews/dream-vegas-sports/",
    "https://www.freebets.com/betting-sites/reviews/sporting-index-sports/",
    "https://www.freebets.com/betting-sites/reviews/fitzdares-sport/",
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
]


class ReviewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_featured_bonus = False
        self.featured_bonus_depth = 0
        self.featured_bonus_text = []
        self.bonus_found = False

        self.in_article = False
        self.article_depth = 0
        self.article_found = False
        self.in_p = False
        self.article_paragraphs = []
        self.current_p = []

        self._depth_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()

        # Detect featured-offer__bonus
        if "featured-offer__bonus" in classes:
            self.in_featured_bonus = True
            self.featured_bonus_depth = len(self._depth_stack)
            self.bonus_found = True

        # Detect article tag (or div with entry-content / article class)
        if tag == "article" or (tag == "div" and any(c in classes for c in ["entry-content", "article-content", "post-content", "article__body"])):
            if not self.article_found:
                self.in_article = True
                self.article_depth = len(self._depth_stack)
                self.article_found = True

        if self.in_article and tag == "p":
            self.in_p = True
            self.current_p = []

        self._depth_stack.append(tag)

    def handle_endtag(self, tag):
        if self._depth_stack:
            self._depth_stack.pop()

        if self.in_featured_bonus and len(self._depth_stack) <= self.featured_bonus_depth:
            self.in_featured_bonus = False

        if self.in_article and tag == "p" and self.in_p:
            text = "".join(self.current_p).strip()
            if text:
                self.article_paragraphs.append(text)
            self.in_p = False
            self.current_p = []

        if self.in_article and len(self._depth_stack) <= self.article_depth:
            self.in_article = False

    def handle_data(self, data):
        if self.in_featured_bonus:
            self.featured_bonus_text.append(data)
        if self.in_article and self.in_p:
            self.current_p.append(data)

    def get_bonus(self):
        return " ".join(" ".join(self.featured_bonus_text).split()).strip()

    def get_article_text(self):
        return " ".join(self.article_paragraphs)


def extract_money(text):
    """Find all £N or £N,NNN patterns."""
    return re.findall(r'£[\d,]+(?:\.\d{2})?', text)


def extract_brand(url):
    slug = url.rstrip("/").split("/")[-1]
    slug = re.sub(r"-sports$|-sport$|-sportsbook$", "", slug)
    return slug.replace("-", " ").title()


def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def audit():
    needs_amending = []
    no_offer = []
    clean = []
    errors = []

    total = len(URLS)
    print(f"Starting audit of {total} pages...\n")

    for i, url in enumerate(URLS, 1):
        brand = extract_brand(url)
        print(f"[{i}/{total}] {brand} ...", end=" ", flush=True)

        html = fetch_page(url)
        if html is None:
            print("ERROR")
            errors.append(brand)
            time.sleep(0.5)
            continue

        parser = ReviewParser()
        try:
            parser.feed(html)
        except Exception:
            pass

        bonus = parser.get_bonus()
        article_text = parser.get_article_text()
        article_amounts = extract_money(article_text)

        if not bonus:
            # No CTA box
            print(f"NO OFFER")
            no_offer.append(brand)
        else:
            cta_amounts = extract_money(bonus)
            if not article_amounts:
                # Evergreen page — no amounts in article
                print(f"CLEAN (evergreen) | CTA: {bonus[:60]}")
                clean.append((brand, bonus, [], "evergreen"))
            elif cta_amounts and not any(a in article_amounts for a in cta_amounts):
                # CTA amounts not found in article
                print(f"NEEDS AMENDING | CTA: {bonus[:60]} | Article: {article_amounts[:5]}")
                needs_amending.append((brand, bonus, article_amounts[:5]))
            else:
                print(f"CLEAN | CTA: {bonus[:60]}")
                clean.append((brand, bonus, article_amounts[:5], "ok"))

        time.sleep(0.5)

    return needs_amending, no_offer, clean, errors, total


if __name__ == "__main__":
    needs_amending, no_offer, clean, errors, total = audit()

    print("\n" + "="*60)
    print("AUDIT SUMMARY")
    print("="*60)
    print(f"\nNeeds amending ({len(needs_amending)}):")
    for brand, offer, amounts in needs_amending:
        print(f"  {brand} — CTA: {offer} | Article: {', '.join(amounts)}")

    print(f"\nNo active offer ({len(no_offer)}):")
    for brand in no_offer:
        print(f"  {brand}")

    print(f"\nClean ({len(clean)}):")
    for item in clean:
        print(f"  {item[0]}")

    if errors:
        print(f"\nErrors ({len(errors)}): {', '.join(errors)}")

    # Write structured results to file for Slack posting
    import json
    results = {
        "total": total,
        "needs_amending": [(b, o, a) for b, o, a in needs_amending],
        "no_offer": no_offer,
        "clean_count": len(clean),
        "errors": errors,
    }
    with open("/tmp/audit_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to /tmp/audit_results.json")
