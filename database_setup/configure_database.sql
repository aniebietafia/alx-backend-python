-- SQL script to create a database and a table with specified columns and constraints
CREATE DATABASE IF NOT EXISTS ALX_prodev;

-- Switch to the newly created database
USE ALX_prodev;

-- Create the user_data table with specified columns and constraints
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age DECIMAL(3, 0) NOT NULL
);

-- Create an index on the user_id column to optimize queries
CREATE INDEX idx_user_id ON user_data(user_id);