"""NHL API client for fetching stats data."""
import requests
import logging
from datetime import datetime, date
from typing import Dict, List, Optional

from config import config

logger = logging.getLogger(__name__)


class NHLAPIClient:
    """Client for interacting with NHL public API."""
    
    def __init__(self):
        """Initialize NHL API client."""
        self.base_url = config.NHL_API_BASE_URL
        self.stats_url = config.NHL_STATS_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NHL-Stats-Tracker/1.0'
        })
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to NHL API."""
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {url}: {e}")
            return None
    
    def get_current_season(self) -> str:
        """Get current NHL season string (e.g., '20232024')."""
        today = date.today()
        # NHL season typically starts in October
        if today.month >= 10:
            return f"{today.year}{today.year + 1}"
        else:
            return f"{today.year - 1}{today.year}"
    
    def get_teams(self) -> Optional[List[Dict]]:
        """Fetch all NHL teams."""
        logger.info("Fetching NHL teams...")
        url = f"{self.base_url}/teams"
        data = self._make_request(url)
        
        if data:
            logger.info(f"Successfully fetched {len(data)} teams")
            return data
        return None
    
    def get_team_roster(self, team_abbr: str, season: Optional[str] = None) -> Optional[Dict]:
        """Fetch team roster for a specific season."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching roster for {team_abbr} - season {season}...")
        url = f"{self.base_url}/roster/{team_abbr}/{season}"
        data = self._make_request(url)
        
        if data:
            logger.info(f"Successfully fetched roster for {team_abbr}")
            return data
        return None
    
    def get_player_stats(self, player_id: int, season: Optional[str] = None) -> Optional[Dict]:
        """Fetch player statistics for a specific season."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching stats for player {player_id} - season {season}...")
        url = f"{self.base_url}/player/{player_id}/landing"
        data = self._make_request(url)
        
        if data:
            logger.info(f"Successfully fetched stats for player {player_id}")
            return data
        return None
    
    def get_team_stats(self, team_abbr: str, season: Optional[str] = None) -> Optional[Dict]:
        """Fetch team statistics for a specific season."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching stats for team {team_abbr} - season {season}...")
        url = f"{self.base_url}/club-stats/{team_abbr}/{season}/2"
        data = self._make_request(url)
        
        if data:
            logger.info(f"Successfully fetched stats for {team_abbr}")
            return data
        return None
    
    def get_standings(self, season: Optional[str] = None) -> Optional[Dict]:
        """Fetch current standings."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching standings for season {season}...")
        url = f"{self.base_url}/standings/{season}"
        data = self._make_request(url)
        
        if data:
            logger.info("Successfully fetched standings")
            return data
        return None
    
    def get_schedule(self, team_abbr: Optional[str] = None, 
                     start_date: Optional[str] = None,
                     end_date: Optional[str] = None) -> Optional[Dict]:
        """Fetch game schedule."""
        logger.info("Fetching schedule...")
        
        if team_abbr:
            # Team-specific schedule
            season = self.get_current_season()
            url = f"{self.base_url}/club-schedule/{team_abbr}/{season}"
        else:
            # League-wide schedule for a date
            if not start_date:
                start_date = datetime.now().strftime('%Y-%m-%d')
            url = f"{self.base_url}/schedule/{start_date}"
        
        data = self._make_request(url)
        
        if data:
            logger.info("Successfully fetched schedule")
            return data
        return None
    
    def get_game_details(self, game_id: int) -> Optional[Dict]:
        """Fetch detailed game information."""
        logger.info(f"Fetching details for game {game_id}...")
        url = f"{self.base_url}/gamecenter/{game_id}/landing"
        data = self._make_request(url)
        
        if data:
            logger.info(f"Successfully fetched game {game_id} details")
            return data
        return None
    
    def get_skater_stats_leaders(self, season: Optional[str] = None, 
                                  stat_type: str = 'points',
                                  limit: int = 100) -> Optional[List[Dict]]:
        """Fetch top skater statistics."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching top {limit} skaters by {stat_type} for season {season}...")
        url = f"{self.stats_url}/skaters"
        
        params = {
            'cayenneExp': f'seasonId={season} and gameTypeId=2',
            'sort': f'[{{\"{stat_type}\":-1}}]',
            'limit': limit
        }
        
        data = self._make_request(url, params=params)
        
        if data and 'data' in data:
            logger.info(f"Successfully fetched {len(data['data'])} skater stats")
            return data['data']
        return None
    
    def get_goalie_stats_leaders(self, season: Optional[str] = None,
                                  limit: int = 50) -> Optional[List[Dict]]:
        """Fetch top goalie statistics."""
        if not season:
            season = self.get_current_season()
        
        logger.info(f"Fetching top {limit} goalies for season {season}...")
        url = f"{self.stats_url}/goalies"
        
        params = {
            'cayenneExp': f'seasonId={season} and gameTypeId=2',
            'sort': '[{"wins":-1}]',
            'limit': limit
        }
        
        data = self._make_request(url, params=params)
        
        if data and 'data' in data:
            logger.info(f"Successfully fetched {len(data['data'])} goalie stats")
            return data['data']
        return None
    
    def close(self):
        """Close the session."""
        self.session.close()
