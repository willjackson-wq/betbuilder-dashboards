# betbuilder-dashboards — Claude instructions

## free-bet-offer.html — daily copy generation

### Day selection rule (IMPORTANT)
When generating the three-day offer page, **never include today**.

The three days must always be:
- **Day 1 (tab 1):** tomorrow (today + 1)
- **Day 2 (tab 2):** day after tomorrow (today + 2)
- **Day 3 (tab 3):** three days from now (today + 3)

Example: if the script runs on Friday, the tabs must show Saturday, Sunday, Monday — NOT Friday, Saturday, Sunday.

### Bookmaker rotation
Monday=Bet365, Tuesday=William Hill, Wednesday=BetMGM, Thursday=Paddy Power, Friday=Betfair, Saturday=Sky Bet, Sunday=Ladbrokes

Apply the rotation to each of the three future days, not to today.

### Deployment
- Commit HTML to current feature branch, then deploy to `dashboard` branch
- GitHub Pages URL: https://willjackson-wq.github.io/betbuilder-dashboards/free-bet-offer.html

### Slack
- Canvas: F0ANZHYGD7G in #fb-page-updates (private channel C0ANL746CB1)
- Post **Day 1 content only** (tomorrow's content — the nearest of the three days) to #fb-page-updates after updating the canvas
  - e.g. script runs Friday → post Saturday's content to Slack
