# NHL Stats Tracker - Database Schema

## Overview

The database is designed to track NHL statistics over time with a normalized relational structure. All tables include timestamps for tracking when records were created and updated.

## Entity Relationship Diagram

```
┌─────────────────┐
│     Teams       │
├─────────────────┤
│ id (PK)         │
│ nhl_id (unique) │
│ name            │
│ abbreviation    │
│ city            │
│ conference      │
│ division        │
│ active          │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴─────────────────────┬──────────────────┐
    │                          │                  │
┌───▼──────────┐      ┌────────▼────────┐  ┌─────▼──────────┐
│   Players    │      │   Team Stats    │  │     Games      │
├──────────────┤      ├─────────────────┤  ├────────────────┤
│ id (PK)      │      │ id (PK)         │  │ id (PK)        │
│ nhl_id       │      │ team_id (FK)    │  │ nhl_id         │
│ first_name   │      │ season          │  │ season         │
│ last_name    │      │ games_played    │  │ game_type      │
│ position     │      │ wins            │  │ game_date      │
│ team_id (FK) │      │ losses          │  │ home_team (FK) │
│ ...          │      │ points          │  │ away_team (FK) │
└──────┬───────┘      │ goals_for       │  │ home_score     │
       │              │ goals_against   │  │ away_score     │
       │ 1:N          │ ...             │  │ game_state     │
       │              └─────────────────┘  └────────────────┘
       │
┌──────▼──────────┐
│  Player Stats   │
├─────────────────┤
│ id (PK)         │
│ player_id (FK)  │
│ season          │
│ team_id (FK)    │
│ games_played    │
│ goals           │
│ assists         │
│ points          │
│ ...             │
│ (goalie stats)  │
└─────────────────┘

┌──────────────────┐
│ Data Fetch Logs  │
├──────────────────┤
│ id (PK)          │
│ fetch_type       │
│ fetch_date       │
│ status           │
│ records_fetched  │
│ error_message    │
│ duration_seconds │
└──────────────────┘
```

## Tables

### Teams
Stores NHL team information.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `nhl_id` (INTEGER, UNIQUE): Official NHL team ID
- `name` (VARCHAR): Full team name (e.g., "Toronto Maple Leafs")
- `abbreviation` (VARCHAR): Team abbreviation (e.g., "TOR")
- `city` (VARCHAR): Team city
- `conference` (VARCHAR): Conference name
- `division` (VARCHAR): Division name
- `active` (BOOLEAN): Whether team is currently active
- `created_at` (TIMESTAMP): Record creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique index on `nhl_id`

### Players
Stores NHL player information.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `nhl_id` (INTEGER, UNIQUE): Official NHL player ID
- `first_name` (VARCHAR): Player's first name
- `last_name` (VARCHAR): Player's last name
- `jersey_number` (INTEGER): Jersey number
- `position` (VARCHAR): Position code (C, LW, RW, D, G)
- `shoots_catches` (VARCHAR): Shooting/catching hand (L/R)
- `height_inches` (INTEGER): Height in inches
- `weight_pounds` (INTEGER): Weight in pounds
- `birth_date` (DATE): Date of birth
- `birth_city` (VARCHAR): Birth city
- `birth_country` (VARCHAR): Birth country
- `nationality` (VARCHAR): Nationality code
- `team_id` (INTEGER, FK): Current team
- `active` (BOOLEAN): Whether player is currently active
- `created_at` (TIMESTAMP): Record creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique index on `nhl_id`
- Composite index on `last_name`, `first_name`

**Foreign Keys:**
- `team_id` → `teams.id`

### Games
Stores NHL game information.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `nhl_id` (INTEGER, UNIQUE): Official NHL game ID
- `season` (VARCHAR): Season identifier (e.g., "20232024")
- `game_type` (VARCHAR): Game type (Regular, Playoff, etc.)
- `game_date` (TIMESTAMP): Date and time of game
- `home_team_id` (INTEGER, FK): Home team
- `away_team_id` (INTEGER, FK): Away team
- `home_score` (INTEGER): Home team score
- `away_score` (INTEGER): Away team score
- `game_state` (VARCHAR): Game state (FINAL, LIVE, SCHEDULED)
- `venue` (VARCHAR): Venue name
- `created_at` (TIMESTAMP): Record creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique index on `nhl_id`
- Index on `game_date`
- Composite index on `game_date`, `home_team_id`, `away_team_id`

**Foreign Keys:**
- `home_team_id` → `teams.id`
- `away_team_id` → `teams.id`

### Player Stats
Stores player statistics by season.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `player_id` (INTEGER, FK): Player reference
- `season` (VARCHAR): Season identifier
- `team_id` (INTEGER, FK): Team during this season
- `games_played` (INTEGER): Games played

**Skater Statistics:**
- `goals` (INTEGER): Goals scored
- `assists` (INTEGER): Assists
- `points` (INTEGER): Total points
- `plus_minus` (INTEGER): Plus/minus rating
- `penalty_minutes` (INTEGER): Penalty minutes
- `power_play_goals` (INTEGER): Power play goals
- `power_play_points` (INTEGER): Power play points
- `short_handed_goals` (INTEGER): Short-handed goals
- `short_handed_points` (INTEGER): Short-handed points
- `game_winning_goals` (INTEGER): Game-winning goals
- `overtime_goals` (INTEGER): Overtime goals
- `shots` (INTEGER): Shots on goal
- `shooting_percentage` (FLOAT): Shooting percentage
- `time_on_ice_per_game` (FLOAT): Average time on ice
- `faceoff_percentage` (FLOAT): Faceoff win percentage

**Goalie Statistics:**
- `wins` (INTEGER): Wins
- `losses` (INTEGER): Losses
- `overtime_losses` (INTEGER): Overtime losses
- `saves` (INTEGER): Saves
- `shots_against` (INTEGER): Shots against
- `goals_against` (INTEGER): Goals against
- `save_percentage` (FLOAT): Save percentage
- `goals_against_average` (FLOAT): Goals against average
- `shutouts` (INTEGER): Shutouts

**Timestamps:**
- `created_at` (TIMESTAMP): Record creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique constraint on `player_id`, `season`
- Composite index on `player_id`, `season`

**Foreign Keys:**
- `player_id` → `players.id`
- `team_id` → `teams.id`

### Team Stats
Stores team statistics by season.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `team_id` (INTEGER, FK): Team reference
- `season` (VARCHAR): Season identifier
- `games_played` (INTEGER): Games played
- `wins` (INTEGER): Wins
- `losses` (INTEGER): Losses
- `overtime_losses` (INTEGER): Overtime losses
- `points` (INTEGER): Total points
- `point_percentage` (FLOAT): Point percentage
- `goals_for` (INTEGER): Goals scored
- `goals_against` (INTEGER): Goals allowed
- `goal_differential` (INTEGER): Goal differential
- `shots_for_per_game` (FLOAT): Average shots per game
- `shots_against_per_game` (FLOAT): Average shots against per game
- `power_play_percentage` (FLOAT): Power play percentage
- `penalty_kill_percentage` (FLOAT): Penalty kill percentage
- `faceoff_win_percentage` (FLOAT): Faceoff win percentage
- `created_at` (TIMESTAMP): Record creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique constraint on `team_id`, `season`
- Composite index on `team_id`, `season`

**Foreign Keys:**
- `team_id` → `teams.id`

### Data Fetch Logs
Audit log of all data fetch operations.

**Columns:**
- `id` (INTEGER, PK): Internal database ID
- `fetch_type` (VARCHAR): Type of fetch (teams, players, games, stats)
- `fetch_date` (TIMESTAMP): When fetch occurred
- `status` (VARCHAR): Status (success, error, partial)
- `records_fetched` (INTEGER): Number of records fetched
- `error_message` (VARCHAR): Error message if failed
- `duration_seconds` (FLOAT): Duration of fetch operation

**Indexes:**
- Primary key on `id`
- Index on `fetch_date`

## Design Principles

1. **Normalization**: Data is normalized to reduce redundancy
2. **Historical Tracking**: Season-based stats allow tracking over time
3. **Referential Integrity**: Foreign keys maintain data consistency
4. **Audit Trail**: Timestamps and fetch logs provide complete audit trail
5. **Flexibility**: Schema supports both skater and goalie statistics
6. **Performance**: Strategic indexes for common query patterns

## Common Queries

### Top Scorers
```sql
SELECT p.first_name, p.last_name, ps.points, ps.goals, ps.assists
FROM players p
JOIN player_stats ps ON p.id = ps.player_id
WHERE ps.season = '20232024'
ORDER BY ps.points DESC
LIMIT 10;
```

### Team Standings
```sql
SELECT t.name, ts.wins, ts.losses, ts.points
FROM teams t
JOIN team_stats ts ON t.id = ts.team_id
WHERE ts.season = '20232024'
ORDER BY ts.points DESC;
```

### Player Career Stats
```sql
SELECT ps.season, ps.games_played, ps.goals, ps.assists, ps.points
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
WHERE p.nhl_id = 8478402
ORDER BY ps.season;
```

### Team Roster
```sql
SELECT p.jersey_number, p.first_name, p.last_name, p.position
FROM players p
JOIN teams t ON p.team_id = t.id
WHERE t.abbreviation = 'TOR'
ORDER BY p.position, p.jersey_number;
```
