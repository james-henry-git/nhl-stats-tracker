"""Data manager for storing NHL stats in the database."""
import logging
from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy.exc import IntegrityError

from database import db
from models import Team, Player, Game, PlayerStats, TeamStats, DataFetchLog
from nhl_api_client import NHLAPIClient

logger = logging.getLogger(__name__)


class DataManager:
    """Manages data fetching and storage operations."""
    
    def __init__(self):
        """Initialize data manager."""
        self.api_client = NHLAPIClient()
    
    def _log_fetch(self, fetch_type: str, status: str, records: int = 0, 
                   error: Optional[str] = None, duration: Optional[float] = None):
        """Log data fetch operation."""
        with db.get_session() as session:
            log = DataFetchLog(
                fetch_type=fetch_type,
                status=status,
                records_fetched=records,
                error_message=error,
                duration_seconds=duration
            )
            session.add(log)
    
    def fetch_and_store_teams(self) -> bool:
        """Fetch all teams and store in database."""
        start_time = datetime.now()
        logger.info("Starting team data fetch...")
        
        try:
            teams_data = self.api_client.get_teams()
            if not teams_data:
                self._log_fetch('teams', 'error', error='No data returned from API')
                return False
            
            with db.get_session() as session:
                count = 0
                for team_data in teams_data:
                    # Check if team exists
                    team = session.query(Team).filter_by(nhl_id=team_data.get('id')).first()

                    # Extract data with fallbacks for both legacy and new API formats
                    team_name = team_data.get('name') or team_data.get('fullName', '')
                    team_abbr = team_data.get('abbreviation') or team_data.get('triCode', '')

                    # Handle venue data (legacy API format)
                    venue = team_data.get('venue', {})
                    team_city = venue.get('city', '') if venue else ''

                    if team:
                        # Update existing team
                        team.name = team_name
                        team.abbreviation = team_abbr
                        team.city = team_city
                        team.updated_at = datetime.utcnow()
                    else:
                        # Create new team
                        team = Team(
                            nhl_id=team_data.get('id'),
                            name=team_name,
                            abbreviation=team_abbr,
                            city=team_city,
                            active=team_data.get('active', True)
                        )
                        session.add(team)

                    count += 1
                
                duration = (datetime.now() - start_time).total_seconds()
                self._log_fetch('teams', 'success', count, duration=duration)
                logger.info(f"Successfully stored {count} teams in {duration:.2f}s")
                return True
                
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)
            self._log_fetch('teams', 'error', error=error_msg, duration=duration)
            logger.error(f"Failed to fetch and store teams: {e}")
            return False
    
    def fetch_and_store_team_roster(self, team_abbr: str, season: Optional[str] = None) -> bool:
        """Fetch team roster and store players."""
        start_time = datetime.now()
        logger.info(f"Starting roster fetch for {team_abbr}...")
        
        try:
            roster_data = self.api_client.get_team_roster(team_abbr, season)
            if not roster_data:
                self._log_fetch('players', 'error', error=f'No roster data for {team_abbr}')
                return False
            
            with db.get_session() as session:
                # Get team from database
                team = session.query(Team).filter_by(abbreviation=team_abbr).first()
                if not team:
                    logger.error(f"Team {team_abbr} not found in database")
                    return False
                
                count = 0
                
                # Process forwards
                for player_data in roster_data.get('forwards', []):
                    self._store_player(session, player_data, team.id)
                    count += 1
                
                # Process defensemen
                for player_data in roster_data.get('defensemen', []):
                    self._store_player(session, player_data, team.id)
                    count += 1
                
                # Process goalies
                for player_data in roster_data.get('goalies', []):
                    self._store_player(session, player_data, team.id)
                    count += 1
                
                duration = (datetime.now() - start_time).total_seconds()
                self._log_fetch('players', 'success', count, duration=duration)
                logger.info(f"Successfully stored {count} players for {team_abbr} in {duration:.2f}s")
                return True
                
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)
            self._log_fetch('players', 'error', error=error_msg, duration=duration)
            logger.error(f"Failed to fetch and store roster for {team_abbr}: {e}")
            return False
    
    def _store_player(self, session, player_data: Dict, team_id: int):
        """Store or update a single player."""
        player_id = player_data.get('id')
        if not player_id:
            return
        
        player = session.query(Player).filter_by(nhl_id=player_id).first()
        
        # Parse birth date
        birth_date = None
        if player_data.get('birthDate'):
            try:
                birth_date = datetime.strptime(player_data['birthDate'], '%Y-%m-%d').date()
            except:
                pass
        
        if player:
            # Update existing player
            player.first_name = player_data.get('firstName', {}).get('default', '')
            player.last_name = player_data.get('lastName', {}).get('default', '')
            player.jersey_number = player_data.get('sweaterNumber')
            player.position = player_data.get('positionCode')
            player.shoots_catches = player_data.get('shootsCatches')
            player.height_inches = player_data.get('heightInInches')
            player.weight_pounds = player_data.get('weightInPounds')
            player.birth_date = birth_date
            player.birth_city = player_data.get('birthCity', {}).get('default', '')
            player.birth_country = player_data.get('birthCountry')
            player.team_id = team_id
            player.updated_at = datetime.utcnow()
        else:
            # Create new player
            player = Player(
                nhl_id=player_id,
                first_name=player_data.get('firstName', {}).get('default', ''),
                last_name=player_data.get('lastName', {}).get('default', ''),
                jersey_number=player_data.get('sweaterNumber'),
                position=player_data.get('positionCode'),
                shoots_catches=player_data.get('shootsCatches'),
                height_inches=player_data.get('heightInInches'),
                weight_pounds=player_data.get('weightInPounds'),
                birth_date=birth_date,
                birth_city=player_data.get('birthCity', {}).get('default', ''),
                birth_country=player_data.get('birthCountry'),
                team_id=team_id,
                active=True
            )
            session.add(player)
    
    def fetch_and_store_team_stats(self, team_abbr: str, season: Optional[str] = None) -> bool:
        """Fetch and store team statistics."""
        start_time = datetime.now()
        if not season:
            season = self.api_client.get_current_season()
        
        logger.info(f"Starting team stats fetch for {team_abbr} - {season}...")
        
        try:
            stats_data = self.api_client.get_team_stats(team_abbr, season)
            if not stats_data:
                self._log_fetch('team_stats', 'error', error=f'No stats for {team_abbr}')
                return False
            
            with db.get_session() as session:
                team = session.query(Team).filter_by(abbreviation=team_abbr).first()
                if not team:
                    logger.error(f"Team {team_abbr} not found in database")
                    return False
                
                # Check if stats record exists
                team_stats = session.query(TeamStats).filter_by(
                    team_id=team.id, season=season
                ).first()
                
                # Extract stats from API response
                standings = stats_data.get('standings', {})
                
                if team_stats:
                    # Update existing stats
                    team_stats.games_played = standings.get('gamesPlayed', 0)
                    team_stats.wins = standings.get('wins', 0)
                    team_stats.losses = standings.get('losses', 0)
                    team_stats.overtime_losses = standings.get('otLosses', 0)
                    team_stats.points = standings.get('points', 0)
                    team_stats.point_percentage = standings.get('pointPctg', 0.0)
                    team_stats.goals_for = standings.get('goalFor', 0)
                    team_stats.goals_against = standings.get('goalAgainst', 0)
                    team_stats.goal_differential = standings.get('goalDifferential', 0)
                    team_stats.updated_at = datetime.utcnow()
                else:
                    # Create new stats record
                    team_stats = TeamStats(
                        team_id=team.id,
                        season=season,
                        games_played=standings.get('gamesPlayed', 0),
                        wins=standings.get('wins', 0),
                        losses=standings.get('losses', 0),
                        overtime_losses=standings.get('otLosses', 0),
                        points=standings.get('points', 0),
                        point_percentage=standings.get('pointPctg', 0.0),
                        goals_for=standings.get('goalFor', 0),
                        goals_against=standings.get('goalAgainst', 0),
                        goal_differential=standings.get('goalDifferential', 0)
                    )
                    session.add(team_stats)
                
                duration = (datetime.now() - start_time).total_seconds()
                self._log_fetch('team_stats', 'success', 1, duration=duration)
                logger.info(f"Successfully stored team stats for {team_abbr} in {duration:.2f}s")
                return True
                
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)
            self._log_fetch('team_stats', 'error', error=error_msg, duration=duration)
            logger.error(f"Failed to fetch and store team stats for {team_abbr}: {e}")
            return False
    
    def fetch_all_teams_data(self, season: Optional[str] = None) -> bool:
        """Fetch teams, rosters, and stats for all teams."""
        logger.info("Starting full data fetch for all teams...")
        
        # First fetch teams
        if not self.fetch_and_store_teams():
            logger.error("Failed to fetch teams")
            return False
        
        # Get all teams from database
        with db.get_session() as session:
            teams = session.query(Team).filter_by(active=True).all()
            team_abbrs = [team.abbreviation for team in teams]
        
        # Fetch roster and stats for each team
        success_count = 0
        for team_abbr in team_abbrs:
            logger.info(f"Processing {team_abbr}...")
            
            if self.fetch_and_store_team_roster(team_abbr, season):
                success_count += 1
            
            if self.fetch_and_store_team_stats(team_abbr, season):
                success_count += 1
        
        logger.info(f"Completed data fetch. Successful operations: {success_count}")
        return True
    
    def close(self):
        """Close API client."""
        self.api_client.close()
