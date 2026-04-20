# BetBuilder Dashboards — Project Instructions

## Overview

This project produces yellow card booking tips for Will Jackson at GDC Group, posted to Slack. The **Daily Card Betting Tips** routine selects players via web search and WhoScored, then enriches each tip with live booking odds from the OpticOdds v3 API.

Do not use emdash. Keep tone informal but informative.

---

## Daily Card Betting Tips Routine

### Step 1 — Determine dates to cover

Check today's day of the week:

- **Monday–Thursday:** cover fixtures for tomorrow only
- **Friday:** cover fixtures for Saturday, Sunday, and Monday

### Step 2 — Find fixtures for each target date

Use WebSearch to find fixtures on each target date across: UEFA Champions League, Europa League, Conference League; Premier League, Championship, League One, League Two; Scottish Premiership, Scottish Championship; La Liga, Ligue 1, Bundesliga, Serie A.

### Step 3 — Select players using WhoScored

For each fixture search: `site:whoscored.com [Team Name] player stats 2025-26`

Select players meeting **all** of these criteria:

- Not listed as injured for this match
- Top 5 in yellow cards for their team this season
- Top 5 in fouls committed for their team this season
- At least one yellow card in their last 5 matches

Target 4–5 tips per day. Don't force weak selections if fixtures are sparse.

### Step 4 — Fetch booking odds via the OpticOdds API

For each selected player, look up their booking odds using the API integration below. This is the only source for odds — never use web search for prices.

1. Identify the fixture in OpticOdds (see API workflow below)
2. Check available markets (`/markets/active`) — look for booking markets such as `player_to_be_carded`, `player_yellow_card`, or `anytime_yellow_card`
3. Fetch odds for the player (do **not** include `is_main=true` for player prop markets)
4. Convert to UK fractional format (see Odds Display Rules)
5. If no booking market is available for a fixture, note `<!-- BOOKING ODDS NOT AVAILABLE -->` and omit the price for that tip — do not guess

### Step 5 — Format the tips

For each selected player:

```
'[Player Name] to be Carded' - [Home Team] vs [Away Team] ([Competition]) — [Fractional Odds] with [Bookmaker]

[3–4 lines: yellow card total, fouls per game, when last carded, why this match sets up a booking]
```

**Writing style rules (no exceptions):**

- Never open a sentence with a numeral. Either write it out ("Seven yellow cards…") or restructure ("Fernandes has 7 yellow cards…")
- Write in full, flowing sentences — not fragments or bullet-point-style clauses. Stats should be woven into prose
- Keep tone casual and editorial — informed but conversational, like a knowledgeable mate making a case
- Lead the analysis by naming the player. Don't open with a bare stat
- Connect sentences with natural transitions so the analysis reads as a paragraph

**Example of what NOT to write:**

> 7 yellow cards this season, joint most at West Ham, backed up by 44 fouls across the campaign. Booked just seven days ago vs Wolves (April 10) and has three yellows in his last five league outings. WhoScored flag him for committing fouls often.

**Example of what TO write:**

> Fernandes has seven yellow cards this season — the joint most at West Ham — backed up by 44 fouls across the campaign. He was booked just seven days ago against Wolves and has picked up three yellows in his last five league outings, marking him out as a repeat offender and prime candidate to be carded. A scrappy Monday night fixture against a combative Palace midfield is exactly the kind of game where he gets his name in the book.

### Step 6 — Post to Slack

Post to `#fb-page-updates`. Use a bold date header per day:

```
🟨 *Card Betting Tips — Friday 18 Apr*

'Player Name to be Carded' - Team A vs Team B (PL) — 5/2 with bet365
[analysis]
```

For Friday runs, include separate headers for Saturday, Sunday, and Monday in one message. Post even if data is partial.

---

## API Integration

Odds are fetched from the OpticOdds v3 API via an n8n workflow proxy. This avoids network allowlist restrictions.

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

### API Workflow for Booking Odds

**Step A — Identify the fixture**

Map the competition to OpticOdds sport and league IDs:

| Competition        | sport    | league                        |
|--------------------|----------|-------------------------------|
| Premier League     | soccer   | england_-_premier_league      |
| Championship       | soccer   | england_-_championship        |
| League One         | soccer   | england_-_league_one          |
| League Two         | soccer   | england_-_league_two          |
| FA Cup             | soccer   | england_-_fa_cup              |
| Champions League   | soccer   | uefa_-_champions_league       |
| Europa League      | soccer   | uefa_-_europa_league          |
| Conference League  | soccer   | uefa_-_conference_league      |
| Scottish Prem      | soccer   | scotland_-_premiership        |
| La Liga            | soccer   | spain_-_la_liga               |
| Ligue 1            | soccer   | france_-_ligue_1              |
| Bundesliga         | soccer   | germany_-_bundesliga          |
| Serie A            | soccer   | italy_-_serie_a               |

If unsure of a league ID, call `/api/v3/leagues?sport=soccer` to list all available leagues.

**Step B — Get the fixture ID**

```
https://api.opticodds.com/api/v3/fixtures?sport={sport}&league={league}&start_date_after={YYYY-MM-DD}&start_date_before={YYYY-MM-DD}
```

Match on `home_team_display` and `away_team_display`. The fixture `id` is required for all subsequent calls.

**Step C — Check available markets**

```
https://api.opticodds.com/api/v3/markets/active?fixture_id={fixture_id}&sportsbook={sportsbook}
```

Confirm a booking market is available before fetching odds. The actual available market in the API is `first_card_receiver` — markets like `player_to_be_carded`, `player_yellow_card`, and `anytime_yellow_card` do not exist. Use `first_card_receiver` for all player booking tips.

**Step D — Fetch booking odds**

```
https://api.opticodds.com/api/v3/fixtures/odds?fixture_id={fixture_id}&sportsbook={sportsbook}&market={market}&odds_format=decimal
```

**Do NOT include `is_main=true`** — it suppresses player prop markets.

---

## Odds Display Rules (UK Market)

All odds must be displayed in **fractional format**. This is non-negotiable.

### How to get fractional odds (in order of preference)

1. **Extract from deep links (preferred):** The API returns `deep_link` URLs for each selection. For bet365, fractional odds appear at the end of the URL after a `~` character (e.g. `~5/2` means the fractional odds are 5/2).

2. **Convert from decimal:** Subtract 1 from the decimal price and express as a simplified fraction:
   - 1.83 → 0.83 → **5/6**
   - 2.00 → 1.00 → **Evens**
   - 3.50 → 2.50 → **5/2**
   - 4.00 → 3.00 → **3/1**
   - Use standard UK fractional odds where close (e.g. round 1.83 to 5/6, not 83/100)

### Display rules

- **Always display fractional odds** in tip text (e.g. `5/2 with bet365`)
- When decimal odds are `2.00`, display as **Evens** (not 1/1)
- Never display American or decimal odds in tip text
- Fractional format is NOT supported by the API — always request `odds_format=decimal` and convert
- Supported API formats: `american`, `decimal`, `probability`, `malay`, `hong_kong`, `indonesian`

Common UK fractional odds: Evens, 10/11, 5/6, 4/5, 8/11, 4/6, 1/2, 11/10, 6/5, 5/4, 11/8, 6/4, 7/4, 2/1, 9/4, 5/2, 11/4, 3/1, 7/2, 4/1, 9/2, 5/1, 6/1, 8/1, 10/1, 12/1, 14/1, 16/1, 20/1, 25/1, 33/1, 50/1

---

## Data Source Rules

| Data type              | Source                  |
|------------------------|-------------------------|
| Fixtures / dates       | WebSearch               |
| Player stats / form    | WhoScored (web search)  |
| Injury status          | WhoScored (web search)  |
| Odds and prices        | OpticOdds API only      |

- **Never use web search for odds.** If the API has no price, omit it — don't estimate or source from another site.
- **Never use the API for player stats.** WhoScored is the source for yellow card counts, fouls, and booking history.

---

## Error Handling

If an API call fails:

1. Report the specific endpoint and HTTP status code.
2. Continue building the tip without odds.
3. Mark the missing price with `<!-- BOOKING ODDS NOT AVAILABLE: {endpoint} -->`.
4. Never fabricate odds. If it didn't come from the API, it doesn't appear in the tip.

**API Parameter Checklist — before every odds call:**

- [ ] `odds_format=decimal` is appended
- [ ] `is_main=true` is **absent** (booking markets are player props)
- [ ] Only one market per API call — do not comma-separate markets
