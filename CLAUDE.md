# Claude Instructions — betbuilder-dashboards

## Free Bet Offer of the Day — Standing Rules

### Offer Research (MANDATORY)
Before writing any welcome offer copy for a bookmaker, **always fetch the offer from the freebets.com review page listed below**. Do not use any other source (search results, training data, previous copy). The offer at the top of the review page is the live, correct offer to write about.

| Bookmaker | Review URL |
|-----------|-----------|
| Betway | https://www.freebets.com/betting-sites/reviews/betway-sports/ |
| Playzee | https://www.freebets.com/betting-sites/reviews/playzee/ |
| BetMGM | https://www.freebets.com/betting-sites/reviews/betmgm-sports/ |
| Paddy Power | https://www.freebets.com/betting-sites/reviews/paddy-power-sports/ |
| tote | https://www.freebets.com/betting-sites/reviews/tote-sports/ |
| bet365 | https://www.freebets.com/betting-sites/reviews/bet365/ |
| Ladbrokes | https://www.freebets.com/betting-sites/reviews/ladbrokes-sports/ |

Fetch all three bookmaker pages in parallel before writing any copy.

### Bookmaker Rotation (by day of week)
Monday=Betway, Tuesday=Playzee, Wednesday=BetMGM, Thursday=Paddy Power, Friday=tote, Saturday=bet365, Sunday=Ladbrokes

The three days to cover are always tomorrow (+1), day after tomorrow (+2), and three days from now (+3). Never include today.

### Process (run in full each time)
1. Identify the three days and their bookmakers from the rotation above
2. Fetch all three freebets.com review pages simultaneously to get current offers
3. Search for UK sporting events on each of the three days (Premier League, Champions/Europa/Conference League, horse racing, other high-profile UK sport)
4. Write copy for all three days using the verified offers
5. Write/update `free-bet-offer.html` with tabbed interface
6. Commit to current branch, then deploy to `dashboard` branch and push
7. Update the "Free Bet Offer of the Day" Slack canvas (ID: F0ATFCG580L) in #fb-page-updates
8. Post tomorrow's content to #fb-page-updates
