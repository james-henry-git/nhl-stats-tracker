"""Configuration management for NHL Stats Tracker."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Database settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'nhl_stats')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    @property
    def DATABASE_URL(self):
        """Construct database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Application settings
    UPDATE_INTERVAL_HOURS = int(os.getenv('UPDATE_INTERVAL_HOURS', '24'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # NHL API settings
    NHL_API_BASE_URL = "https://api-web.nhle.com/v1"
    NHL_STATS_API_BASE_URL = "https://api.nhle.com/stats/rest/en"


config = Config()
