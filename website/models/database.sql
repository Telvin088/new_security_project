-- Create the database
CREATE DATABASE IF NOT EXISTS security_auth;

-- Use the database
USE security_auth;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    profile_photo VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);


INSERT INTO users (username, email, profile_photo, password) VALUES
('john_doe', 'john.doe@example.com', 'john_doe.jpg', 'hashed_password_1'),
('jane_doe', 'jane.doe@example.com', 'jane_doe.jpg', 'hashed_password_2'),
('alice_smith', 'alice.smith@example.com', 'alice_smith.jpg', 'hashed_password_3'),
('bob_johnson', 'bob.johnson@example.com', 'bob_johnson.jpg', 'hashed_password_4'),
('emma_jones', 'emma.jones@example.com', 'emma_jones.jpg', 'hashed_password_5'),
('michael_brown', 'michael.brown@example.com', 'michael_brown.jpg', 'hashed_password_6'),
('olivia_davis', 'olivia.davis@example.com', 'olivia_davis.jpg', 'hashed_password_7'),
('william_miller', 'william.miller@example.com', 'william_miller.jpg', 'hashed_password_8'),
('sophia_wilson', 'sophia.wilson@example.com', 'sophia_wilson.jpg', 'hashed_password_9'),
('james_taylor', 'james.taylor@example.com', 'james_taylor.jpg', 'hashed_password_10'),
('charlotte_clark', 'charlotte.clark@example.com', 'charlotte_clark.jpg', 'hashed_password_11'),
('david_hall', 'david.hall@example.com', 'david_hall.jpg', 'hashed_password_12'),
('ava_thomas', 'ava.thomas@example.com', 'ava_thomas.jpg', 'hashed_password_13'),
('oliver_walker', 'oliver.walker@example.com', 'oliver_walker.jpg', 'hashed_password_14'),
('amelia_adams', 'amelia.adams@example.com', 'amelia_adams.jpg', 'hashed_password_15'),
('jack_lewis', 'jack.lewis@example.com', 'jack_lewis.jpg', 'hashed_password_16'),
('isabella_evans', 'isabella.evans@example.com', 'isabella_evans.jpg', 'hashed_password_17'),
('ethan_white', 'ethan.white@example.com', 'ethan_white.jpg', 'hashed_password_18'),
('mia_harris', 'mia.harris@example.com', 'mia_harris.jpg', 'hashed_password_19'),
('mason_martin', 'mason.martin@example.com', 'mason_martin.jpg', 'hashed_password_20'),
('harper_thompson', 'harper.thompson@example.com', 'harper_thompson.jpg', 'hashed_password_21'),
('noah_garcia', 'noah.garcia@example.com', 'noah_garcia.jpg', 'hashed_password_22'),
('violet_robinson', 'violet.robinson@example.com', 'violet_robinson.jpg', 'hashed_password_23'),
('lucas_hall', 'lucas.hall@example.com', 'lucas_hall.jpg', 'hashed_password_24'),
('amelia_baker', 'amelia.baker@example.com', 'amelia_baker.jpg', 'hashed_password_25'),
('emma_hill', 'emma.hill@example.com', 'emma_hill.jpg', 'hashed_password_26'),
('ethan_young', 'ethan.young@example.com', 'ethan_young.jpg', 'hashed_password_27'),
('mia_rodriguez', 'mia.rodriguez@example.com', 'mia_rodriguez.jpg', 'hashed_password_28'),
('liam_king', 'liam.king@example.com', 'liam_king.jpg', 'hashed_password_29'),
('ava_flores', 'ava.flores@example.com', 'ava_flores.jpg', 'hashed_password_30'),
('jacob_harris', 'jacob.harris@example.com', 'jacob_harris.jpg', 'hashed_password_31'),
('charlotte_wood', 'charlotte.wood@example.com', 'charlotte_wood.jpg', 'hashed_password_32'),
('oliver_rivera', 'oliver.rivera@example.com', 'oliver_rivera.jpg', 'hashed_password_33'),
('isabella_cooper', 'isabella.cooper@example.com', 'isabella_cooper.jpg', 'hashed_password_34'),
('william_long', 'william.long@example.com', 'william_long.jpg', 'hashed_password_35'),
('harper_gonzalez', 'harper.gonzalez@example.com', 'harper_gonzalez.jpg', 'hashed_password_36'),
('mason_johnson', 'mason.johnson@example.com', 'mason_johnson.jpg', 'hashed_password_37'),
('ava_jackson', 'ava.jackson@example.com', 'ava_jackson.jpg', 'hashed_password_38'),
('mia_torres', 'mia.torres@example.com', 'mia_torres.jpg', 'hashed_password_39'),
('noah_moore', 'noah.moore@example.com', 'noah_moore.jpg', 'hashed_password_40'),
('emma_wright', 'emma.wright@example.com', 'emma_wright.jpg', 'hashed_password_41'),
('liam_anderson', 'liam.anderson@example.com', 'liam_anderson.jpg', 'hashed_password_42'),
('olivia_perez', 'olivia.perez@example.com', 'olivia_perez.jpg', 'hashed_password_43');



USE security_auth;

-- Create the table for the incident report
CREATE TABLE incident_report (
    incident_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    
    -- Incident information
    incident_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    incident_location VARCHAR(255) NOT NULL,
    incident_description TEXT NOT NULL,
    
    -- Category information
    type_of_violence ENUM('Physical Assault', 'Verbal Abuse', 'Other') NOT NULL,
    severity_level ENUM('Low', 'Medium', 'High') NOT NULL,
    injuries_sustained BOOLEAN NOT NULL,
    medical_attention_required BOOLEAN NOT NULL,
    
    -- Victim information
    victim_name VARCHAR(255) NOT NULL,
    victim_age INT NOT NULL,
    victim_gender VARCHAR(50) NOT NULL,
    victim_contact_info VARCHAR(255) NOT NULL,
    
    -- Perpetrator information
    perpetrator_name VARCHAR(255),
    perpetrator_age INT,
    perpetrator_gender VARCHAR(50),
    perpetrator_description TEXT
);

-- Inserting records with specified datetime values
INSERT INTO incident_report (
    incident_datetime,
    incident_location,
    incident_description,
    type_of_violence,
    severity_level,
    injuries_sustained,
    medical_attention_required,
    victim_name,
    victim_age,
    victim_gender,
    victim_contact_info,
    perpetrator_name,
    perpetrator_age,
    perpetrator_gender,
    perpetrator_description
) VALUES
-- Last Monday's date (3 records)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 6) % 7 DAY), 'Location 1', 'Description 1', 'Physical Assault', 'Medium', 0, 0, 'Victim 1', 30, 'Male', 'Contact 1', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 6) % 7 DAY), 'Location 2', 'Description 2', 'Verbal Abuse', 'Low', 0, 0, 'Victim 2', 25, 'Female', 'Contact 2', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 6) % 7 DAY), 'Location 3', 'Description 3', 'Other', 'High', 1, 1, 'Victim 3', 35, 'Male', 'Contact 3', NULL, NULL, NULL, NULL),
-- Last Tuesday's date (5 records)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 5) % 7 DAY), 'Location 4', 'Description 4', 'Physical Assault', 'High', 1, 1, 'Victim 4', 40, 'Female', 'Contact 4', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 5) % 7 DAY), 'Location 5', 'Description 5', 'Verbal Abuse', 'Medium', 0, 0, 'Victim 5', 22, 'Male', 'Contact 5', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 5) % 7 DAY), 'Location 6', 'Description 6', 'Other', 'Low', 0, 0, 'Victim 6', 28, 'Female', 'Contact 6', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 5) % 7 DAY), 'Location 7', 'Description 7', 'Physical Assault', 'High', 1, 1, 'Victim 7', 32, 'Male', 'Contact 7', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 5) % 7 DAY), 'Location 8', 'Description 8', 'Verbal Abuse', 'Low', 0, 0, 'Victim 8', 26, 'Female', 'Contact 8', NULL, NULL, NULL, NULL),
-- Last Wednesday's date (2 records)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 4) % 7 DAY), 'Location 9', 'Description 9', 'Other', 'Medium', 1, 1, 'Victim 9', 37, 'Male', 'Contact 9', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 4) % 7 DAY), 'Location 10', 'Description 10', 'Physical Assault', 'Low', 0, 0, 'Victim 10', 20, 'Female', 'Contact 10', NULL, NULL, NULL, NULL),
-- Last Thursday's date (1 record)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 3) % 7 DAY), 'Location 11', 'Description 11', 'Verbal Abuse', 'High', 0, 0, 'Victim 11', 45, 'Male', 'Contact 11', NULL, NULL, NULL, NULL),
-- Last Friday's date (1 record)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 2) % 7 DAY), 'Location 12', 'Description 12', 'Physical Assault', 'Medium', 1, 1, 'Victim 12', 29, 'Female', 'Contact 12', NULL, NULL, NULL, NULL),
-- Last Saturday's date (3 records)
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 1) % 7 DAY), 'Location 13', 'Description 13', 'Verbal Abuse', 'High', 0, 0, 'Victim 13', 33, 'Male', 'Contact 13', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 1) % 7 DAY), 'Location 14', 'Description 14', 'Other', 'Low', 0, 0, 'Victim 14', 27, 'Female', 'Contact 14', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL (DAYOFWEEK(CURRENT_DATE()) + 1) % 7 DAY), 'Location 15', 'Description 15', 'Physical Assault', 'Medium', 1, 1, 'Victim 15', 42, 'Male', 'Contact 15', NULL, NULL, NULL, NULL),
-- Last Sunday's date (2 records)
(DATE_SUB(CURRENT_DATE(), INTERVAL DAYOFWEEK(CURRENT_DATE()) DAY), 'Location 16', 'Description 16', 'Verbal Abuse', 'Low', 0, 0, 'Victim 16', 30, 'Male', 'Contact 16', NULL, NULL, NULL, NULL),
(DATE_SUB(CURRENT_DATE(), INTERVAL DAYOFWEEK(CURRENT_DATE()) DAY), 'Location 17', 'Description 17', 'Physical Assault', 'Medium', 1, 1, 'Victim 17', 35, 'Female', 'Contact 17', NULL, NULL, NULL, NULL);


use security_auth;

CREATE TABLE TheftReports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    incident_datetime DATETIME,
    incident_location VARCHAR(255),
    incident_description TEXT,
    items_stolen VARCHAR(255),
    estimated_value DECIMAL(10, 2),
    theft_method VARCHAR(100),
    security_measures TEXT,
    security_cameras VARCHAR(255),
    witness_name VARCHAR(100),
    witness_statement TEXT
);


INSERT INTO TheftReports (incident_datetime, incident_location, incident_description, items_stolen, estimated_value, theft_method, security_measures, security_cameras, witness_name, witness_statement)
VALUES
('2024-06-01 14:30:00', '123 Main St', 'Burglary at residence', 'Jewelry, electronics', 5000.00, 'External Theft', 'Locked doors and windows', 'Security cameras covering the front entrance', 'John Doe', 'Saw two masked individuals running from the house.'),
('2024-06-02 09:00:00', '456 Elm St', 'Theft from parked car', 'Wallet, cellphone', 800.00, 'Other', 'None', NULL, 'Jane Smith', 'Heard breaking glass and saw someone reach into the car.'),
('2024-06-03 17:45:00', '789 Oak St', 'Shoplifting at grocery store', 'Various groceries', 100.00, 'Employee Theft', 'Security tags on high-value items', 'Security cameras in all aisles', 'Bob Johnson', 'Saw the person hiding items in their bag.'),
('2024-06-04 12:15:00', '321 Pine St', 'Robbery at convenience store', 'Cash, cigarettes', 500.00, 'External Theft', 'Panic button behind the counter', 'Security cameras covering the cash register', NULL, NULL),
('2024-06-05 16:00:00', '567 Maple St', 'Theft from construction site', 'Power tools, copper wire', 1200.00, 'Other', 'Locked toolboxes', NULL, NULL, NULL),
('2024-06-06 11:30:00', '890 Cedar St', 'Bike theft', 'Mountain bike', 600.00, 'External Theft', 'Bike lock', NULL, NULL, NULL),
('2024-06-07 08:45:00', '234 Walnut St', 'Break-in at office building', 'Laptops, monitors', 3000.00, 'External Theft', 'Security guards on-site', 'Security cameras in lobby and hallways', NULL, NULL),
('2024-06-08 15:20:00', '876 Birch St', 'Package theft from front porch', 'Delivered package', 50.00, 'Other', 'Home security system with cameras', NULL, NULL, NULL),
('2024-06-09 10:10:00', '543 Spruce St', 'Jewelry theft from hotel room', 'Necklaces, rings', 2000.00, 'Employee Theft', 'Lockboxes for valuables', NULL, NULL, NULL),
('2024-06-10 14:00:00', '210 Oak St', 'Credit card theft', 'Credit cards', 0.00, 'Other', 'Shredding sensitive documents', NULL, NULL, NULL),
('2024-06-11 13:30:00', '876 Pine St', 'Break-in at apartment complex', 'TV, gaming console', 700.00, 'External Theft', 'Fenced perimeter with gate', 'Security cameras at entrance', NULL, NULL),
('2024-06-12 11:45:00', '432 Elm St', 'Carjacking', 'Vehicle', 15000.00, 'Other', 'Car alarm system', NULL, NULL, NULL),
('2024-06-13 16:40:00', '789 Maple St', 'Pickpocketing at train station', 'Wallet, passport', 200.00, 'Other', 'Traveling in groups', NULL, NULL, NULL),
('2024-06-14 09:25:00', '654 Cedar St', 'Theft from school classroom', 'Tablet, textbooks', 600.00, 'External Theft', 'Locked classroom doors', 'Security cameras in hallways', NULL, NULL),
('2024-06-15 17:15:00', '321 Walnut St', 'Theft from pharmacy', 'Prescription drugs', 300.00, 'Employee Theft', 'Controlled access to drug storage', 'Security cameras at pharmacy counter', NULL, NULL),
('2024-06-16 10:05:00', '987 Birch St', 'Laptop theft from coffee shop', 'Laptop', 1000.00, 'External Theft', 'Locked cabinets for laptops', 'Security cameras covering seating area', NULL, NULL),
('2024-06-17 15:55:00', '210 Spruce St', 'Break-in at jewelry store', 'Diamond rings, watches', 50000.00, 'Other', 'Vault for high-value items', 'Security cameras covering display cases', NULL, NULL),
('2024-06-18 12:20:00', '876 Pine St', 'Package theft from apartment lobby', 'Delivered package', 30.00, 'External Theft', 'Secure package lockers', 'Security cameras in lobby', NULL, NULL),
('2024-06-19 14:35:00', '543 Elm St', 'Robbery at bank', 'Cash', 10000.00, 'External Theft', 'Bulletproof glass at teller windows', 'Security cameras covering lobby', NULL, NULL),
('2024-06-20 08:10:00', '210 Oak St', 'Car break-in at parking garage', 'GPS, sunglasses', 150.00, 'External Theft', 'Security patrols in garage', 'Security cameras covering parking areas', NULL, NULL),
('2024-06-21 16:30:00', '654 Walnut St', 'Theft from clothing store', 'Designer clothing', 800.00, 'Employee Theft', 'Security tags on clothing', 'Security cameras covering store floor', NULL, NULL),
('2024-06-22 11:40:00', '987 Cedar St', 'Bike theft from college campus', 'Road bike', 1000.00, 'External Theft', 'Bike racks with locks', 'Security cameras covering bike racks', NULL, NULL),
('2024-06-23 14:50:00', '123 Elm St', 'Break-in at restaurant', 'Cash register, alcohol', 700.00, 'External Theft', 'Locking cash register drawers', 'Security cameras covering entrances', NULL, NULL);

use security_auth;
CREATE TABLE damage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    incident_datetime DATETIME NOT NULL,
    incident_location VARCHAR(255) NOT NULL,
    incident_description TEXT NOT NULL,
    damage_type VARCHAR(100) NOT NULL,
    estimated_cost DECIMAL(10, 2) NOT NULL,
    damage_cause VARCHAR(100) NOT NULL,
    preventive_measures TEXT,
    security_cameras TEXT,
    witness_name VARCHAR(100),
    witness_statement TEXT,
    session_id VARCHAR(255)
);
