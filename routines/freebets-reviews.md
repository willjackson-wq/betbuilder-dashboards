# Freebets Reviews Routine

**Schedule:** Every Monday at 8:30 BST  
**Slack channel:** #fb-page-updates

## Instructions

Every Monday morning, crawl through every page under:  
`https://www.freebets.com/betting-sites/reviews/`

For example:
- `https://www.freebets.com/betting-sites/reviews/bet365-sports/`
- `https://www.freebets.com/betting-sites/reviews/paddy-power-sports/`

For each brand page, check that the offer in the article body matches the offer in the CTA at the top of the page.

Example: for Paddy Power, the H1 is "Bet £5 Get £40" — this should match the CTA and the content of the article.

Once all pages have been checked, post a brief summary to `#fb-page-updates` stating which pages need amending. If everything is consistent, say it's a clean run and no urgent action is required.

## Technical notes

- All HTTP requests must include a browser User-Agent header (e.g. `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`) — the site returns 503 without it.
- Page content including CTAs and article body text is server-rendered and fully readable from the raw HTTP response.
