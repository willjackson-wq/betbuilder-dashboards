# BetBuilder Dashboards — Project Instructions

## Overview

This project produces betting tip articles for FreeBets.com. The primary routine is **Daily Card Betting Tips**, which generates match preview and betting tip content driven entirely by live data from the OpticOdds v3 API.

---

## Daily Card Betting Tips Routine

When asked to produce a Daily Card Betting Tips article (or any betting tip content), follow the full workflow below. Every factual claim must come from the API. No exceptions.

---

## API Integration

Data is fetched from the OpticOdds v3 API via an n8n workflow proxy. This avoids network allowlist restrictions.

### n8n Workflow Proxy

The workflow accepts a webhook POST with a `url` field containing the full OpticOdds v3 API URL. Call it using `n8n:execute_workflow`.

**Calling pattern:**

```
n8n:execute_workflow
  workflowId: "2Ki8OH2pDXd7J0DI"
  inputs:
    type: "webhook"
    webhookData:
      method: "POST"
      body:
        url: "https://api.opticodds.com/api/v3/{endpoint}?{params}"
```

**Important:** Always drop `is_main=true` from the URL when fetching player prop markets (`anytime_goal_scorer`, `player_to_score_or_assist`, etc.) — that filter suppresses props. Only use `is_main=true` for main markets (`moneyline`, `total_goals`, `asian_handicap`).

---

## Data Fetching Workflow

For every article, follow this sequence. All calls pass a full URL in the `url` body field.

### Step 1 — Identify sport and league

Map the user's request to OpticOdds sport and league IDs. League IDs use the format `country_-_league_name`.

Common mappings:

| Competition        | sport     | league                          |
|--------------------|-----------|----------------------------------|
| Premier League     | soccer    | england_-_premier_league         |
| Championship       | soccer    | england_-_championship           |
| FA Cup             | soccer    | england_-_fa_cup                 |
| Champions League   | soccer    | uefa_-_champions_league          |
| La Liga            | soccer    | spain_-_la_liga                  |
| NFL                | football  | nfl                              |

If unsure, call `/api/v3/leagues?sport={sport}` to list all available leagues.

### Step 2 — Get upcoming fixtures

```
https://api.opticodds.com/api/v3/fixtures?sport={sport}&league={league}&start_date_after={YYYY-MM-DD}&start_date_before={YYYY-MM-DD}
```

Parse the response to find the fixture matching the user's request. Use `start_date`, team names (`home_team_display`, `away_team_display`), and `id` (fixture ID).

### Step 2b — Get recent results (form data)

```
https://api.opticodds.com/api/v3/fixtures?sport={sport}&league={league}&start_date_after={14_days_ago}&start_date_before={today}
```

Filter returned fixtures by team name in `home_team_display` or `away_team_display`. **Always use this endpoint for recent results and form data. Never rely on web search for scores.**

### Step 3 — Get available markets for a fixture

```
https://api.opticodds.com/api/v3/markets/active?fixture_id={fixture_id}&sportsbook={sportsbook}
```

Use this to confirm which market IDs are available before fetching odds.

### Step 4 — Get odds: main markets

```
https://api.opticodds.com/api/v3/fixtures/odds?fixture_id={fixture_id}&sportsbook={sportsbook}&market={market}&is_main=true&odds_format=decimal
```

Use `is_main=true` for main markets only: `moneyline`, `asian_handicap`, `total_goals`.

### Step 5 — Get odds: player props

```
https://api.opticodds.com/api/v3/fixtures/odds?fixture_id={fixture_id}&sportsbook={sportsbook}&market={market}&odds_format=decimal
```

**Do NOT include `is_main=true`** for player prop markets — it suppresses all results. Markets include: `anytime_goal_scorer`, `first_goal_scorer`, `last_goal_scorer`, `player_to_score_or_assist`, `player_goals`.

### Step 6 — Get injuries (if available)

```
https://api.opticodds.com/api/v3/injuries?sport={sport}&league={league}
```

---

## Odds Display Rules (UK Market)

This is a **UK market** publication. All odds must be displayed in **fractional format** as the primary display. This is non-negotiable for FreeBets.com content.

### How to get fractional odds (in order of preference)

1. **Extract from deep links (preferred):** The API returns `deep_link` URLs for each selection. For bet365, the fractional odds appear at the end of the URL after a `~` character (e.g. `~17/20` means fractional odds are 17/20). Always extract from here first.

2. **Convert from decimal:** If no deep link is available, subtract 1 from the decimal price and express as a simplified fraction:
   - 1.83 → 0.83 → **5/6**
   - 2.00 → 1.00 → **Evens**
   - 3.70 → 2.70 → **27/10**
   - 4.20 → 3.20 → **16/5**
   - Use standard UK fractional odds where close (e.g. round 1.83 to 5/6, not 83/100)

### Display rules

- **Primary display**: Fractional odds in article body text and table cells (e.g. `17/20`, `27/10`, `16/5`)
- **Secondary display**: Decimal odds in the `title` attribute of table cells as a hover tooltip (e.g. `<td title="1.83">17/20</td>`)
- **Never** display American or decimal odds in article body text. Decimal is for tooltips only.
- When decimal odds are `2.00` / American `+100`, display as **Evens** (not 1/1)
- Fractional format is NOT supported by the API — always request `odds_format=decimal` and convert
- Supported API formats: `american`, `decimal`, `probability`, `malay`, `hong_kong`, `indonesian`

Common UK fractional odds reference: Evens, 10/11, 5/6, 4/5, 8/11, 4/6, 1/2, 11/10, 6/5, 5/4, 11/8, 6/4, 7/4, 2/1, 9/4, 5/2, 11/4, 3/1, 7/2, 4/1, 9/2, 5/1, 6/1, 8/1, 10/1, 12/1, 14/1, 16/1, 20/1, 25/1, 33/1, 50/1

---

## Factual Data Rule (Critical)

**Every factual claim in an article MUST come from the OpticOdds API. No exceptions, except league standings as noted below.**

This rule exists because web search results are frequently inaccurate for live sports data (wrong scores, outdated standings, incorrect team news). The API is the only verified source.

**What counts as a factual claim:**
- Match scores and results
- Recent form (W/D/L sequences)
- Odds and prices
- Fixture dates, kick-off times, venues
- Team names and abbreviations
- Injury news (player, type, status)

**Rules:**
1. If a fact can be pulled from the API, it **must** be pulled from the API. Never use web search for data the API provides.
2. If a fact **cannot** be pulled from the API (e.g. transfer rumours, tactical analysis, historical records beyond API range), do **not** include it in the article. Leave it out entirely.
3. Never guess, estimate, or infer factual data. If the API returns empty, say nothing rather than something wrong.
4. Never use web search to supplement or verify API data. The API is the source of truth.
5. If the API does not have enough data to write a complete article, write a shorter article with only what the API provides. A shorter accurate article is always better than a longer inaccurate one.
6. Commentary, opinion and betting analysis are fine (e.g. "that price looks generous", "this could be a tight game"). These are not factual claims. But they must be grounded in API data, not assumptions.

### Narrow Exception: League Standings

The OpticOdds API does not provide league standings. For this data **only**, web search is permitted under strict conditions:

- Source **must** be one of: `premierleague.com`, BBC Sport (`bbc.co.uk/sport`), or Sky Sports (`skysports.com`). No other sources.
- Data permitted: league position, points total, games played, W/D/L record, goal difference. Nothing else from web search.
- Add an HTML comment in the output: `<!-- STANDINGS DATA FROM WEB SEARCH - MANUAL CHECK REQUIRED -->`
- If web search returns conflicting data from different sources, do **not** include it. Flag the conflict to the user.

---

## Error Handling

If an API call fails:

1. Report the specific endpoint that failed and the HTTP status code.
2. Continue with available data where possible.
3. Mark unpopulated sections with `<!-- DATA UNAVAILABLE: {endpoint} -->`.
4. Never fabricate any data. If it didn't come from the API, it doesn't go in the article.

**When data is missing:**
- Odds not yet available: write `<!-- ODDS NOT YET AVAILABLE FOR THIS FIXTURE -->` and skip the odds table.
- Recent results unavailable: do not mention form at all. Do not guess from web search.
- Fixture not found: tell the user. Do not write an article without the fixture data.

---

## API Parameter Checklist

Before making any odds call, verify:

- [ ] `odds_format=decimal` is appended (fractional is not supported; convert after)
- [ ] `is_main=true` is included for main markets (`moneyline`, `total_goals`, `asian_handicap`)
- [ ] `is_main=true` is **absent** for player props (`anytime_goal_scorer`, `player_to_score_or_assist`, etc.)
- [ ] Only one market per API call — do not comma-separate markets
