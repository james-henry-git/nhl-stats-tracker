"""Configuration management for NHL Stats Tracker."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # Database settings - SQLite
    DB_PATH = os.getenv('DB_PATH', 'nhl_stats.db')

    @property
    def DATABASE_URL(self):
        """Construct database URL."""
        return f"sqlite:///{self.DB_PATH}"
    
    # Application settings
    UPDATE_INTERVAL_HOURS = int(os.getenv('UPDATE_INTERVAL_HOURS', '24'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # NHL API settings
    NHL_API_BASE_URL = "https://api-web.nhle.com/v1"
    NHL_STATS_API_BASE_URL = "https://api.nhle.com/stats/rest/en"
    NHL_LEGACY_API_BASE_URL = "https://statsapi.web.nhl.com/api/v1"  # Legacy API for teams list


config = Config()
