-- SQL script to add is_admin column to users table
ALTER TABLE users
ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
