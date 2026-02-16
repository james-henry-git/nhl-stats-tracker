-- NHL Stats Tracker Database Setup Script
-- Run this script to create the database and user

-- Create database
CREATE DATABASE nhl_stats;

-- Create user (optional - update password as needed)
-- CREATE USER nhl_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
-- GRANT ALL PRIVILEGES ON DATABASE nhl_stats TO nhl_user;

-- Connect to the database
\c nhl_stats;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created automatically by SQLAlchemy when you run the application
-- This script is just for initial database setup
