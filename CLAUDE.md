# betbuilder-dashboards — Claude instructions

## Free Bet Offer of the Day (`free-bet-offer.html`)

### Bookmaker rotation (by day of week)
Monday=betway, Tuesday=playzee, Wednesday=BetMGM, Thursday=Paddy Power, Friday=tote, Saturday=bet365, Sunday=Ladbrokes

### Slack posting rules

**All days except Friday:** Post tomorrow's content only as a standalone message to `#fb-page-updates`.

**Friday only:** Post all three days in a single Slack thread to `#fb-page-updates`:
- **Main message** — Saturday's content (tomorrow)
- **Reply 1** — Sunday's content, posted as a direct reply to the Saturday message (`thread_ts` = Saturday message timestamp)
- **Reply 2** — Monday's content, posted as a direct reply to the Saturday message (`thread_ts` = Saturday message timestamp)

Both Sunday and Monday replies sit flat under Saturday — do not chain them (do not reply to Sunday with Monday).

