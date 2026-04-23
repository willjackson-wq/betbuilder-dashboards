# betbuilder-dashboards

This repo contains routine instructions and configuration for automated monitoring tasks on freebets.com.

## Freebets Reviews Routine

A weekly Monday audit that checks every brand review page on freebets.com to ensure the offer shown in the CTA box matches what's written in the article body.

Full instructions: `routines/freebets-reviews.md`

### Key facts from setup

- **75 brand review pages** exist under `freebets.com/betting-sites/reviews/`
- The index page (`/betting-sites/reviews/`) only shows 8 brands — the rest are JS-rendered. Always use the **sitemap** to get the full URL list: `https://www.freebets.com/sitemap.xml`
- The site blocks requests without a browser User-Agent header (returns 503). Always set: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`
- Fetch pages **sequentially with ~0.5s delay** — concurrent fetching triggers rate limiting
- Page content (CTAs, article body) is **server-rendered** and readable from raw HTTP — no headless browser needed
- The CTA offer text lives in the **`featured-offer__bonus`** CSS class

### Matching logic

| Situation | Action |
|---|---|
| CTA amounts differ from article amounts | Flag as needing amendment |
| Article has no monetary amounts at all | Include in check but don't flag — intentionally evergreen |
| CTA box missing entirely | List separately — brand has no active offer, monitor for return |

### Slack output

Post results to `#fb-page-updates` when the crawl is complete (no fixed deadline after the 8:30 start).

See `routines/freebets-reviews.md` for the exact message format.
