#!/usr/bin/env python3
"""Freebets review page auditor — fetches each review, checks CTA vs article body amounts."""

import re
import time
import urllib.request

from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
SITEMAP = "https://www.freebets.com/sitemap.xml"
REVIEW_PREFIX = "https://www.freebets.com/betting-sites/reviews/"
AMOUNT_RE = re.compile(r"£\s*\d[\d,]*(?:\.\d+)?")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def get_review_urls():
    xml = fetch(SITEMAP)
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    urls = [
        u for u in locs
        if u.startswith(REVIEW_PREFIX)
        and u.rstrip("/") != REVIEW_PREFIX.rstrip("/")
    ]
    return sorted(urls)


def brand_from_url(url):
    slug = url.rstrip("/").split("/")[-1]
    # prettify slug → brand name
    slug = slug.replace("-sports", "").replace("-sport", "")
    return slug.replace("-", " ").title()


def extract_cta(soup):
    """Return the text of .featured-offer__bonus, or None if absent."""
    el = soup.find(class_="featured-offer__bonus")
    if el:
        return el.get_text(" ", strip=True)
    return None


def extract_article_amounts(soup):
    """Return all £ amounts found in article body paragraphs."""
    # Try common article containers
    article = (
        soup.find("article")
        or soup.find(class_=re.compile(r"entry-content|post-content|article-body|review"))
        or soup.find("main")
    )
    if not article:
        article = soup

    amounts = []
    for p in article.find_all(["p", "li", "h2", "h3", "h4"]):
        amounts.extend(AMOUNT_RE.findall(p.get_text()))
    return list(dict.fromkeys(amounts))  # deduplicated, order-preserved


def extract_cta_amounts(cta_text):
    if not cta_text:
        return []
    return AMOUNT_RE.findall(cta_text)


def audit():
    urls = get_review_urls()
    print(f"Found {len(urls)} review pages to audit.\n")

    needs_amending = []   # CTA exists, amounts not in body
    no_offer = []         # CTA element missing
    clean = []            # everything OK or evergreen

    for i, url in enumerate(urls, 1):
        brand = brand_from_url(url)
        print(f"[{i}/{len(urls)}] {brand} …", end=" ", flush=True)
        try:
            html = fetch(url)
            soup = BeautifulSoup(html, "lxml")

            cta = extract_cta(soup)
            article_amounts = extract_article_amounts(soup)
            cta_amounts = extract_cta_amounts(cta)

            if cta is None:
                # No active offer
                no_offer.append(brand)
                print("NO OFFER")
            elif not article_amounts:
                # Evergreen page — no amounts anywhere in article
                clean.append(brand)
                print(f"EVERGREEN (CTA: {cta!r})")
            else:
                # Check whether CTA amounts appear somewhere in the article body
                cta_in_body = any(a in article_amounts for a in cta_amounts)
                if cta_amounts and not cta_in_body:
                    needs_amending.append({
                        "brand": brand,
                        "cta": cta,
                        "article_amounts": article_amounts,
                    })
                    print(f"NEEDS AMENDING — CTA: {cta!r} | Body: {article_amounts}")
                else:
                    clean.append(brand)
                    print(f"CLEAN (CTA: {cta!r})")

        except Exception as e:
            print(f"ERROR: {e}")
            needs_amending.append({
                "brand": brand,
                "cta": f"[fetch error: {e}]",
                "article_amounts": [],
            })

        if i < len(urls):
            time.sleep(0.5)

    return urls, needs_amending, no_offer, clean


def build_slack_message(total, needs_amending, no_offer, clean):
    from datetime import date
    today = date.today()
    day_name = today.strftime("%A")
    date_str = today.strftime("%-d %B %Y")

    lines = [
        f"*Freebets Reviews Audit — {day_name} {date_str}*",
        f"Checked {total} pages under freebets.com/betting-sites/reviews/",
        "",
    ]

    if needs_amending:
        lines.append("*Pages where CTA doesn't match article (needs amending):*")
        for item in needs_amending:
            amounts_str = ", ".join(item["article_amounts"][:6])
            if len(item["article_amounts"]) > 6:
                amounts_str += " …"
            lines.append(f"• {item['brand']} — CTA: {item['cta']} | Article mentions: {amounts_str}")
        lines.append("")

    if no_offer:
        lines.append("*No active offer (monitor for return):*")
        for brand in no_offer:
            lines.append(f"• {brand}")
        lines.append("")

    n_clean = len(clean)
    lines.append(f"Clean run for remaining {n_clean} pages — no action required.")

    return "\n".join(lines)


if __name__ == "__main__":
    urls, needs_amending, no_offer, clean = audit()
    total = len(urls)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {total} pages checked")
    print(f"  Needs amending : {len(needs_amending)}")
    print(f"  No active offer: {len(no_offer)}")
    print(f"  Clean          : {len(clean)}")
    print("=" * 60 + "\n")

    msg = build_slack_message(total, needs_amending, no_offer, clean)
    print("SLACK MESSAGE PREVIEW:")
    print(msg)

    # Save message to file so the caller can pick it up
    with open("/tmp/slack_message.txt", "w") as f:
        f.write(msg)
    print("\nMessage saved to /tmp/slack_message.txt")
