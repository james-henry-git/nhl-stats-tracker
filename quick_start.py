"""Quick start script for NHL Stats Tracker - demonstrates basic usage."""
import logging
from database import db
from data_manager import DataManager
from config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Quick start demonstration."""
    print("\n" + "=" * 60)
    print("NHL STATS TRACKER - QUICK START")
    print("=" * 60 + "\n")
    
    # Initialize database
    print("Step 1: Initializing database connection...")
    db.initialize()
    db.create_tables()
    print("✓ Database initialized\n")
    
    # Create data manager
    data_manager = DataManager()
    
    try:
        # Fetch teams
        print("Step 2: Fetching NHL teams...")
        if data_manager.fetch_and_store_teams():
            print("✓ Teams fetched and stored\n")
        else:
            print("✗ Failed to fetch teams\n")
            return
        
        # Fetch data for a few popular teams
        teams_to_fetch = ['TOR', 'MTL', 'BOS', 'NYR', 'EDM']
        
        print(f"Step 3: Fetching rosters and stats for {len(teams_to_fetch)} teams...")
        print(f"Teams: {', '.join(teams_to_fetch)}\n")
        
        for team_abbr in teams_to_fetch:
            print(f"Processing {team_abbr}...")
            
            # Fetch roster
            if data_manager.fetch_and_store_team_roster(team_abbr):
                print(f"  ✓ Roster fetched")
            else:
                print(f"  ✗ Roster failed")
            
            # Fetch stats
            if data_manager.fetch_and_store_team_stats(team_abbr):
                print(f"  ✓ Stats fetched")
            else:
                print(f"  ✗ Stats failed")
            
            print()
        
        # Show summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        from models import Team, Player, TeamStats
        
        with db.get_session() as session:
            team_count = session.query(Team).count()
            player_count = session.query(Player).count()
            stats_count = session.query(TeamStats).count()
            
            print(f"Teams in database:       {team_count}")
            print(f"Players in database:     {player_count}")
            print(f"Team stats records:      {stats_count}")
        
        print("=" * 60)
        print("\nQuick start completed successfully!")
        print("\nNext steps:")
        print("  - Run 'python main.py fetch-all' to fetch all teams")
        print("  - Run 'python main.py stats' to see database statistics")
        print("  - Run 'python main.py schedule' for automated updates")
        print("  - See README.md for more commands and usage\n")
        
    except Exception as e:
        logger.error(f"Error during quick start: {e}", exc_info=True)
    finally:
        data_manager.close()
        db.close()


if __name__ == '__main__':
    main()
