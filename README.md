# NHL Stats Tracker

A comprehensive Python application to download, store, and track NHL statistics over time using the official NHL public API and SQLite database.

## Features

- **Automated Data Collection**: Fetch NHL teams, players, rosters, and statistics from the official NHL API
- **SQLite Database**: Lightweight local storage with proper relational schema - no server required
- **Scheduled Updates**: Automatic daily updates of statistics
- **Comprehensive Stats**: Track player stats, team stats, games, and more
- **Time-Series Tracking**: Monitor statistics changes over multiple seasons
- **Logging**: Complete audit trail of all data fetch operations

## Database Schema

The system tracks:
- **Teams**: NHL team information (name, abbreviation, division, conference)
- **Players**: Player details (name, position, physical stats, birthplace)
- **Games**: Game results and schedules
- **Player Stats**: Season-by-season player statistics (goals, assists, points, etc.)
- **Team Stats**: Season-by-season team statistics (wins, losses, goals for/against, etc.)
- **Data Fetch Logs**: Audit trail of all data collection operations

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

That's it! SQLite is included with Python, so no separate database installation needed.

## Installation

### 1. Clone or Download the Project

```bash

cd nhl-stats-tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

The app works out of the box with default settings. If you want to customize:

```bash
cp .env.example .env
```

Edit `.env` file with your preferences:

```env
# Optional: specify database file location (defaults to nhl_stats.db)
DB_PATH=nhl_stats.db
UPDATE_INTERVAL_HOURS=24
LOG_LEVEL=INFO
```

### 5. Initialize Database Tables

```bash
python main.py init
```

## Usage

### Command Line Interface

The application provides several commands:

#### Initialize Database
```bash
python main.py init
```

#### Fetch All NHL Teams
```bash
python main.py fetch-teams
```

#### Fetch Team Roster
```bash
# Current season
python main.py fetch-roster TOR

# Specific season
python main.py fetch-roster TOR --season 20232024
```

#### Fetch Team Statistics
```bash
# Current season
python main.py fetch-stats TOR

# Specific season
python main.py fetch-stats TOR --season 20232024
```

#### Fetch All Data (Teams, Rosters, and Stats)
```bash
# Current season
python main.py fetch-all

# Specific season
python main.py fetch-all --season 20232024
```

#### Show Database Statistics
```bash
python main.py stats
```

#### Run Scheduled Updates
```bash
python main.py schedule
```

This will:
1. Run an initial data fetch
2. Schedule daily updates at 3:00 AM
3. Continue running until stopped with Ctrl+C

### Team Abbreviations

Common NHL team abbreviations:
- **TOR** - Toronto Maple Leafs
- **MTL** - Montreal Canadiens
- **BOS** - Boston Bruins
- **NYR** - New York Rangers
- **CHI** - Chicago Blackhawks
- **DET** - Detroit Red Wings
- **EDM** - Edmonton Oilers
- **VAN** - Vancouver Canucks
- **CGY** - Calgary Flames
- **LAK** - Los Angeles Kings

And many more! Run `python main.py fetch-teams` to get all teams.

## Project Structure

```
nhl-stats-tracker/
├── config.py              # Configuration management
├── models.py              # SQLAlchemy database models
├── database.py            # Database connection and session management
├── nhl_api_client.py      # NHL API client
├── data_manager.py        # Data fetching and storage logic
├── scheduler.py           # Scheduled update system
├── main.py                # Main CLI application
├── requirements.txt       # Python dependencies
├── setup_database.sql     # Database setup script
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## API Endpoints Used

The application uses the official NHL public API:
- **Base URL**: `https://api-web.nhle.com/v1`
- **Stats URL**: `https://api.nhle.com/stats/rest/en`

Key endpoints:
- `/teams` - All NHL teams
- `/roster/{team}/{season}` - Team roster
- `/club-stats/{team}/{season}/2` - Team statistics
- `/player/{id}/landing` - Player details and stats
- `/standings/{season}` - League standings
- `/schedule/{date}` - Game schedule

## Database Queries

### Example Queries

Get top scorers for current season:
```sql
SELECT p.first_name, p.last_name, ps.goals, ps.assists, ps.points
FROM players p
JOIN player_stats ps ON p.id = ps.player_id
WHERE ps.season = '20232024'
ORDER BY ps.points DESC
LIMIT 10;
```

Get team standings:
```sql
SELECT t.name, ts.wins, ts.losses, ts.overtime_losses, ts.points
FROM teams t
JOIN team_stats ts ON t.id = ts.team_id
WHERE ts.season = '20232024'
ORDER BY ts.points DESC;
```

Track player performance over time:
```sql
SELECT ps.season, ps.games_played, ps.goals, ps.assists, ps.points
FROM player_stats ps
JOIN players p ON ps.player_id = p.id
WHERE p.first_name = 'Connor' AND p.last_name = 'McDavid'
ORDER BY ps.season;
```

## Logging

All operations are logged to:
- **Console**: Real-time output
- **File**: `nhl_stats_tracker.log` (main operations)
- **File**: `nhl_stats_scheduler.log` (scheduled updates)

## Troubleshooting

### Database Issues
- The SQLite database file (`nhl_stats.db`) is created automatically on first run
- If you get database errors, try deleting `nhl_stats.db` and running `python main.py init` again
- The database file can be moved/backed up like any other file

### API Request Failures
- Check internet connection
- NHL API may have rate limits (the client includes delays)
- Some endpoints may change - check NHL API documentation

### Missing Data
- Some historical data may not be available via API
- Player stats are only available for seasons they played
- Team abbreviations must be exact (case-sensitive)

## Future Enhancements

Potential improvements:
- Web dashboard for visualizing stats
- Player comparison tools
- Advanced analytics and predictions
- Game-by-game statistics
- Real-time game updates
- Export to CSV/Excel
- REST API for accessing stored data

## License

This project is for educational and personal use. NHL statistics are property of the National Hockey League.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- NHL for providing the public API
- SQLAlchemy for excellent ORM capabilities
- SQLite for lightweight, reliable data storage
```