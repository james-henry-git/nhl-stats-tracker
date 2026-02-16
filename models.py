"""Database models for NHL Stats Tracker."""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, 
    ForeignKey, Boolean, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Team(Base):
    """NHL Team model."""
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    nhl_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    city = Column(String(100))
    conference = Column(String(50))
    division = Column(String(50))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    players = relationship("Player", back_populates="team")
    team_stats = relationship("TeamStats", back_populates="team")
    games_home = relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    games_away = relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")


class Player(Base):
    """NHL Player model."""
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    nhl_id = Column(Integer, unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    jersey_number = Column(Integer)
    position = Column(String(10))
    shoots_catches = Column(String(1))  # L or R
    height_inches = Column(Integer)
    weight_pounds = Column(Integer)
    birth_date = Column(Date)
    birth_city = Column(String(100))
    birth_country = Column(String(100))
    nationality = Column(String(10))
    team_id = Column(Integer, ForeignKey('teams.id'))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="players")
    player_stats = relationship("PlayerStats", back_populates="player")
    
    __table_args__ = (
        Index('idx_player_name', 'last_name', 'first_name'),
    )


class Game(Base):
    """NHL Game model."""
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    nhl_id = Column(Integer, unique=True, nullable=False, index=True)
    season = Column(String(10), nullable=False)  # e.g., "20232024"
    game_type = Column(String(10))  # Regular, Playoff, etc.
    game_date = Column(DateTime, nullable=False, index=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    home_score = Column(Integer)
    away_score = Column(Integer)
    game_state = Column(String(20))  # FINAL, LIVE, SCHEDULED, etc.
    venue = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="games_home")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="games_away")
    
    __table_args__ = (
        Index('idx_game_date_teams', 'game_date', 'home_team_id', 'away_team_id'),
    )


class PlayerStats(Base):
    """Player statistics by season."""
    __tablename__ = 'player_stats'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    season = Column(String(10), nullable=False)  # e.g., "20232024"
    team_id = Column(Integer, ForeignKey('teams.id'))
    games_played = Column(Integer, default=0)
    
    # Skater stats
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    points = Column(Integer, default=0)
    plus_minus = Column(Integer, default=0)
    penalty_minutes = Column(Integer, default=0)
    power_play_goals = Column(Integer, default=0)
    power_play_points = Column(Integer, default=0)
    short_handed_goals = Column(Integer, default=0)
    short_handed_points = Column(Integer, default=0)
    game_winning_goals = Column(Integer, default=0)
    overtime_goals = Column(Integer, default=0)
    shots = Column(Integer, default=0)
    shooting_percentage = Column(Float)
    time_on_ice_per_game = Column(Float)
    faceoff_percentage = Column(Float)
    
    # Goalie stats
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    overtime_losses = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    shots_against = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    save_percentage = Column(Float)
    goals_against_average = Column(Float)
    shutouts = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="player_stats")
    
    __table_args__ = (
        UniqueConstraint('player_id', 'season', name='uq_player_season'),
        Index('idx_player_season', 'player_id', 'season'),
    )


class TeamStats(Base):
    """Team statistics by season."""
    __tablename__ = 'team_stats'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    season = Column(String(10), nullable=False)
    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    overtime_losses = Column(Integer, default=0)
    points = Column(Integer, default=0)
    point_percentage = Column(Float)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_differential = Column(Integer, default=0)
    shots_for_per_game = Column(Float)
    shots_against_per_game = Column(Float)
    power_play_percentage = Column(Float)
    penalty_kill_percentage = Column(Float)
    faceoff_win_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="team_stats")
    
    __table_args__ = (
        UniqueConstraint('team_id', 'season', name='uq_team_season'),
        Index('idx_team_season', 'team_id', 'season'),
    )


class DataFetchLog(Base):
    """Log of data fetch operations."""
    __tablename__ = 'data_fetch_logs'
    
    id = Column(Integer, primary_key=True)
    fetch_type = Column(String(50), nullable=False)  # teams, players, games, stats
    fetch_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = Column(String(20), nullable=False)  # success, error, partial
    records_fetched = Column(Integer, default=0)
    error_message = Column(String(500))
    duration_seconds = Column(Float)
