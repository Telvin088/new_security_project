-- Create the database
CREATE DATABASE new_security_auth;

-- Use the database
USE new_security_auth;

-- Create the users table
CREATE TABLE
    users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(255),
        username VARCHAR(255) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL,
        profile_photo VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

-- Use the database
USE new_security_auth;

CREATE TABLE
    reports (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        incident_id VARCHAR(50) UNIQUE NOT NULL, -- Unique incident_id column
        date_time DATETIME NOT NULL,
        issue_type VARCHAR(50) NOT NULL,
        victim_name VARCHAR(100),
        victim_age INTEGER,
        witness VARCHAR(100),
        incident_description TEXT,
        username VARCHAR(255),
        session_id VARCHAR(255),
        status VARCHAR(255) NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

USE new_security_auth;

CREATE TABLE
    theft_reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        incident_id VARCHAR(50) UNIQUE NOT NULL, -- Unique incident_id column
        date_time DATE,
        stolen_items VARCHAR(255),
        stolen_value VARCHAR(255),
        theft_description TEXT,
        username VARCHAR(255),
        session_id VARCHAR(255),
        status VARCHAR(255) NOT NULL DEFAULT 'pending',
        created_at DATE DEFAULT CURRENT_DATE
    );

USE new_security_auth;

CREATE TABLE
    damages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        incident_id VARCHAR(50) UNIQUE NOT NULL, -- Unique incident_id column
        date_time DATETIME NOT NULL,
        items_destroyed INT NOT NULL,
        value_of_destroyed DECIMAL(10, 2) NOT NULL,
        damage_description TEXT,
        estimated_repair DECIMAL(10, 2) NOT NULL,
        username VARCHAR(255) NOT NULL,
        status VARCHAR(255) NOT NULL DEFAULT 'pending',
        session_id VARCHAR(255) NOT NULL
    );

use new_security_auth;

CREATE TABLE
    IF NOT EXISTS contact_messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20),
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

use new_security_auth;

CREATE TABLE
    messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        session_id VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

USE new_security_auth;

CREATE TABLE incident_assignments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  assign_date DATE NOT NULL,
  username VARCHAR(255) NOT NULL,
  notes TEXT,
  session_id VARCHAR(255) NOT NULL,
  incident_id VARCHAR(255) NOT NULL,
  FOREIGN KEY (username) REFERENCES users(username)  -- Notice the parentheses around users(username)
);


use new_security_auth;
CREATE TABLE solved_incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    incident_id INT NOT NULL,
    assign_date VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    notes TEXT NOT NULL,
    incident_data JSON NOT NULL
);


-- pip install flask flask-mysqldb reportlab
-- pip install Flask pymysql
