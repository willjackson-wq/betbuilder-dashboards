# Freebets Reviews Routine

**Schedule:** Every Monday at 8:30 BST  
**Slack channel:** #fb-page-updates

## What to do

### 1. Get all brand review URLs

Fetch `https://www.freebets.com/sitemap.xml` and extract every URL that matches the pattern `freebets.com/betting-sites/reviews/[slug]/`. Do not use the index page — it only shows 8 of the 75 brands.

### 2. Fetch and check each page

For each URL, make an HTTP GET request with this User-Agent header:
`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`

Wait 0.5 seconds between each request to avoid rate limiting.

From each page, extract:
- The **CTA offer text** — found in the HTML element with CSS class `featured-offer__bonus`
- Any **monetary amounts** (e.g. £10, £30, £40) mentioned in the article body paragraphs

Then apply this logic:
- If the CTA box is **missing** → the brand has no active offer. Add it to the "no active offer" list.
- If the CTA contains monetary amounts that **do not appear anywhere in the article body** → add it to the "needs amending" list, noting the CTA offer and what the article says instead.
- If the article body contains **no monetary amounts at all** → the page is intentionally evergreen. Mark it as clean.
- Otherwise → mark as clean.

### 3. Post to Slack

Post the results to the Slack channel `#fb-page-updates` using this format:

> **Freebets Reviews Audit — Monday [date]**
>
> Checked [n] pages under freebets.com/betting-sites/reviews/
>
> **Pages where CTA offer doesn't match article content (needs amending):**
> • [brand] — CTA: [offer] | Article mentions [amounts found]
> *(If none: "None — all checked pages are consistent")*
>
> **No active offer (CTA box missing — monitor for when deals return):**
> [brand list]
>
> **Clean run for remaining [n] pages — no action required.**
