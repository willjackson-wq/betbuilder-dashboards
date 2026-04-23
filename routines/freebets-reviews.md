# Freebets Reviews Routine

**Schedule:** Every Monday at 8:30 BST  
**Slack channel:** #fb-page-updates

## Instructions

Every Monday morning, crawl through every brand review page on freebets.com and check that the offer in the CTA box matches the offer mentioned in the article body.

### Step 1 — Get the full page list

Fetch the sitemap to get all review URLs (the index page only shows 8 brands as the rest are JS-rendered):

```
https://www.freebets.com/sitemap.xml
```

Extract all URLs matching `freebets.com/betting-sites/reviews/[slug]/`.

### Step 2 — Check each page

For each URL, fetch the page and extract:
- **CTA offer**: the text in the `featured-offer__bonus` CSS class
- **Article amounts**: any monetary values (e.g. £10, £30) in the article body paragraphs

**Matching logic:**
- If the CTA offer contains monetary amounts that do NOT appear anywhere in the article body → flag as needing amendment
- If the article body contains no monetary amounts at all → still include in the weekly check but do not flag as an error (these pages are written to be evergreen, which is intentional)
- If the CTA box is missing entirely → the brand has no active offer; list it separately for monitoring (a new offer may appear in future weeks)

### Step 3 — Post to Slack

Once all pages are checked, post a summary to `#fb-page-updates` in this format:

> **Freebets Reviews Audit — Monday [date]**
>
> Checked [n] pages under freebets.com/betting-sites/reviews/
>
> **Pages where CTA offer doesn't match article content (needs amending):**
> • [brand] — CTA: [offer] | Article mentions [amounts]
> *(or "None — clean run" if no mismatches)*
>
> **No active offer (CTA box missing — monitor for when deals return):**
> [brand list]
>
> **Clean run for remaining [n] pages — no action required.**

## Technical notes

- All HTTP requests must include a browser User-Agent header (e.g. `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`) — the site returns 503 without it.
- Fetch pages sequentially with a short delay (~0.5s) between requests. Concurrent fetching triggers rate limiting and causes 503 errors.
- Page content including CTAs and article body text is server-rendered and fully readable from the raw HTTP response.
- The CTA offer text lives in the `featured-offer__bonus` CSS class.
