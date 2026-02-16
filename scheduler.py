"""Scheduler for periodic NHL stats updates."""
import schedule
import time
import logging
from datetime import datetime

from database import db
from data_manager import DataManager
from config import config

logger = logging.getLogger(__name__)


class StatsScheduler:
    """Scheduler for automated stats updates."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.data_manager = DataManager()
        self.running = False
    
    def update_all_stats(self):
        """Update all NHL stats."""
        logger.info("=" * 60)
        logger.info(f"Starting scheduled stats update at {datetime.now()}")
        logger.info("=" * 60)
        
        try:
            self.data_manager.fetch_all_teams_data()
            logger.info("Scheduled stats update completed successfully")
        except Exception as e:
            logger.error(f"Error during scheduled update: {e}")
    
    def setup_schedule(self):
        """Configure the update schedule."""
        # Schedule daily updates
        update_time = "03:00"  # 3 AM
        schedule.every().day.at(update_time).do(self.update_all_stats)
        
        logger.info(f"Scheduler configured to run daily at {update_time}")
        logger.info(f"Update interval: {config.UPDATE_INTERVAL_HOURS} hours")
    
    def run(self):
        """Run the scheduler."""
        self.running = True
        self.setup_schedule()
        
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        # Run initial update
        logger.info("Running initial stats update...")
        self.update_all_stats()
        
        # Keep running scheduled tasks
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            self.stop()
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        self.data_manager.close()
        logger.info("Scheduler stopped")


def main():
    """Main entry point for scheduler."""
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('nhl_stats_scheduler.log'),
            logging.StreamHandler()
        ]
    )
    
    # Initialize database
    logger.info("Initializing database connection...")
    db.initialize()
    
    # Create tables if they don't exist
    logger.info("Creating database tables if needed...")
    db.create_tables()
    
    # Start scheduler
    scheduler = StatsScheduler()
    scheduler.run()


if __name__ == '__main__':
    main()
