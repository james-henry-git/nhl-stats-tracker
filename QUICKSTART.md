# Quick Start Guide

Get NHL stats tracking in 3 simple steps!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Initialize the Database

```bash
python main.py init
```

This creates a local SQLite database file (`nhl_stats.db`) - no server setup needed!

## 3. Fetch Some Data

```bash
# Get all NHL teams
python main.py fetch-teams

# Get current Toronto Maple Leafs roster
python main.py fetch-roster TOR

# Get all data for current season
python main.py fetch-all
```

## Done!

Your database now contains NHL data. Use the example queries in README.md to explore it, or build your own analytics!

### Bonus: Automated Updates

Want daily updates? Run:

```bash
python main.py schedule
```

This will update stats every 24 hours automatically.
