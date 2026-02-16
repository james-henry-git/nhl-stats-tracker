"""Main entry point for NHL Stats Tracker."""
import argparse
import logging
import sys

from database import db
from data_manager import DataManager
from config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nhl_stats_tracker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def init_database():
    """Initialize database and create tables."""
    logger.info("Initializing database...")
    db.initialize()
    db.create_tables()
    logger.info("Database initialized successfully")


def fetch_teams():
    """Fetch and store all NHL teams."""
    logger.info("Fetching NHL teams...")
    data_manager = DataManager()
    try:
        success = data_manager.fetch_and_store_teams()
        if success:
            logger.info("Teams fetched successfully")
        else:
            logger.error("Failed to fetch teams")
        return success
    finally:
        data_manager.close()


def fetch_roster(team_abbr: str, season: str = None):
    """Fetch and store team roster."""
    logger.info(f"Fetching roster for {team_abbr}...")
    data_manager = DataManager()
    try:
        success = data_manager.fetch_and_store_team_roster(team_abbr, season)
        if success:
            logger.info(f"Roster for {team_abbr} fetched successfully")
        else:
            logger.error(f"Failed to fetch roster for {team_abbr}")
        return success
    finally:
        data_manager.close()


def fetch_team_stats(team_abbr: str, season: str = None):
    """Fetch and store team statistics."""
    logger.info(f"Fetching stats for {team_abbr}...")
    data_manager = DataManager()
    try:
        success = data_manager.fetch_and_store_team_stats(team_abbr, season)
        if success:
            logger.info(f"Stats for {team_abbr} fetched successfully")
        else:
            logger.error(f"Failed to fetch stats for {team_abbr}")
        return success
    finally:
        data_manager.close()


def fetch_all():
    """Fetch all data (teams, rosters, stats)."""
    logger.info("Fetching all NHL data...")
    data_manager = DataManager()
    try:
        success = data_manager.fetch_all_teams_data()
        if success:
            logger.info("All data fetched successfully")
        else:
            logger.error("Failed to fetch all data")
        return success
    finally:
        data_manager.close()


def show_stats():
    """Display database statistics."""
    from models import Team, Player, TeamStats, DataFetchLog
    
    with db.get_session() as session:
        team_count = session.query(Team).count()
        player_count = session.query(Player).count()
        stats_count = session.query(TeamStats).count()
        
        print("\n" + "=" * 50)
        print("NHL STATS TRACKER - DATABASE STATISTICS")
        print("=" * 50)
        print(f"Teams:        {team_count}")
        print(f"Players:      {player_count}")
        print(f"Team Stats:   {stats_count}")
        print("=" * 50)
        
        # Show recent fetch logs
        recent_logs = session.query(DataFetchLog).order_by(
            DataFetchLog.fetch_date.desc()
        ).limit(10).all()
        
        if recent_logs:
            print("\nRecent Data Fetches:")
            print("-" * 50)
            for log in recent_logs:
                status_symbol = "✓" if log.status == "success" else "✗"
                print(f"{status_symbol} {log.fetch_type:12} | {log.fetch_date.strftime('%Y-%m-%d %H:%M')} | "
                      f"Records: {log.records_fetched:4} | Duration: {log.duration_seconds:.2f}s")
        print("=" * 50 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='NHL Stats Tracker - Download and track NHL statistics'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    subparsers.add_parser('init', help='Initialize database')
    
    # Fetch teams command
    subparsers.add_parser('fetch-teams', help='Fetch all NHL teams')
    
    # Fetch roster command
    roster_parser = subparsers.add_parser('fetch-roster', help='Fetch team roster')
    roster_parser.add_argument('team', help='Team abbreviation (e.g., TOR, MTL)')
    roster_parser.add_argument('--season', help='Season (e.g., 20232024)', default=None)
    
    # Fetch team stats command
    stats_parser = subparsers.add_parser('fetch-stats', help='Fetch team statistics')
    stats_parser.add_argument('team', help='Team abbreviation (e.g., TOR, MTL)')
    stats_parser.add_argument('--season', help='Season (e.g., 20232024)', default=None)
    
    # Fetch all command
    fetch_all_parser = subparsers.add_parser('fetch-all', help='Fetch all data (teams, rosters, stats)')
    fetch_all_parser.add_argument('--season', help='Season (e.g., 20232024)', default=None)
    
    # Show stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Schedule command
    subparsers.add_parser('schedule', help='Run scheduled updates')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize database connection for all commands
    db.initialize()
    
    try:
        if args.command == 'init':
            init_database()
        
        elif args.command == 'fetch-teams':
            fetch_teams()
        
        elif args.command == 'fetch-roster':
            fetch_roster(args.team, args.season)
        
        elif args.command == 'fetch-stats':
            fetch_team_stats(args.team, args.season)
        
        elif args.command == 'fetch-all':
            fetch_all()
        
        elif args.command == 'stats':
            show_stats()
        
        elif args.command == 'schedule':
            from scheduler import main as scheduler_main
            scheduler_main()
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        db.close()


if __name__ == '__main__':
    main()
