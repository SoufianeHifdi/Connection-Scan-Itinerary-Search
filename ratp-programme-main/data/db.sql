SET sql_mode = "";
DROP DATABASE IF EXISTS ratp;

CREATE DATABASE ratp;
USE ratp;

-- CREER ET REMPLIR LES TABLES

-- TABLE AGENCY

CREATE TABLE agency(
	agency_id VARCHAR(255) NOT NULL,
	agency_name TEXT NOT NULL,
	agency_url VARCHAR(255) NOT NULL,
	agency_timezone VARCHAR(15) NOT NULL,
	agency_lang VARCHAR(255) NULL,
	agency_phone VARCHAR(30) NULL,
	agency_email VARCHAR(255) NULL,
	PRIMARY KEY(agency_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\agency.txt'  
INTO TABLE agency 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE CALENDAR

CREATE TABLE calendar(
	service_id VARCHAR(255) NOT NULL,
	monday INT NOT NULL,
	tuesday INT NOT NULL,
	wednesday INT NOT NULL,
	thursday INT NOT NULL,
	friday INT NOT NULL,
	saturday INT NOT NULL,
	sunday INT NOT NULL,
	start_date VARCHAR(8) NOT NULL,
	end_date VARCHAR(8) NOT NULL,
	PRIMARY KEY(service_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\calendar.txt' 
INTO TABLE calendar
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE CALENDAR_DATES

CREATE TABLE calendar_dates(
	service_id VARCHAR(255) NOT NULL,
	calendar_date VARCHAR(8) NOT NULL,
	exception_type INT NOT NULL,
	PRIMARY KEY(service_id,calendar_date)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\calendar_dates.txt' 
INTO TABLE calendar_dates
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE PATHWAYS

CREATE TABLE pathways(
	pathways_id VARCHAR(255) NOT NULL,
	from_stop_id VARCHAR(255) NOT NULL,
	to_stop_id VARCHAR(255) NOT NULL,
	pathway_mode INT NOT NULL,
	is_bidirectional INT NOT NULL,
	pathway_length DECIMAL(10,4) NULL,
	transversal_time INT NULL,
	stair_count INT NULL,
	max_slope INT NULL,
	min_windth INT NULL,
	signposted_as TEXT NULL,
	reversed_signposted_as TEXT NULL,
	PRIMARY KEY(pathways_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\pathways.txt' 
INTO TABLE pathways
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE ROUTES

CREATE TABLE routes(
	route_id VARCHAR(255) NOT NULL,
	agency_id VARCHAR(255) NOT NULL,
	route_short_name VARCHAR(20) NOT NULL,
	route_long_name TEXT NOT NULL,
	route_desc TEXT NULL,
	route_type INT NOT NULL,
	route_url VARCHAR(255) NULL,
	route_color CHAR(6) NULL,
	route_text_color CHAR(6) NULL,
	route_sort_order INT NULL,
	PRIMARY KEY(route_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\routes.txt' 
INTO TABLE routes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE STOPS

CREATE TABLE stops(
	stop_id VARCHAR(255) NOT NULL,
	stop_code TEXT NULL,
	stop_name TEXT NOT NULL,
	stop_desc TEXT NULL,
	stop_lat DECIMAL(20,16) NOT NULL,
	stop_lon DECIMAL(20,16) NOT NULL,
	zone_id INT NOT NULL,
	stop_url VARCHAR(255) NULL,
	location_type INT NULL,
	parent_station VARCHAR(255) NOT NULL,
	wheelchair_boarding INT NULL,
	stop_timezone VARCHAR(20) NULL,
	level_id INT NULL,
	platform_code TEXT NULL,
	PRIMARY KEY(stop_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\stops.txt' 
INTO TABLE stops
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE STOP_TIMES

CREATE TABLE stop_times(
	trip_id VARCHAR(255) NOT NULL,
	arrival_time TIME NOT NULL,
	departure_time TIME NOT NULL,
	stop_id VARCHAR(255) NOT NULL,
	stop_sequence INT NOT NULL,
	pickup_type INT NULL,
	drop_off_type INT NULL,
	local_zone_id INT NULL,
	stop_headsign TEXT NULL,
	timepoint INT NULL
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\stop_times.txt' 
INTO TABLE stop_times
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE TRANSFERS

CREATE TABLE transfers(
	from_stop_id VARCHAR(255) NOT NULL,
	to_stop_id VARCHAR(255) NOT NULL,
	transfer_type INT NOT NULL,
	min_transfer_time INT NOT NULL,
	PRIMARY KEY(from_stop_id,to_stop_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\transfers.txt' 
INTO TABLE transfers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- TABLE TRIPS

CREATE TABLE trips(
	route_id VARCHAR(255) NOT NULL,
	service_id VARCHAR(255) NOT NULL,
	trip_id VARCHAR(255) NOT NULL,
	trip_headsign TEXT NULL,
	trip_short_name TEXT NULL,
	direction_id INT NULL,
	block_id INT NULL,
	shape_id VARCHAR(255) NOT NULL,
	wheelchair_accessible INT NULL,
	bikes_allowed INT NULL,
	PRIMARY KEY(route_id,trip_id)
);
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\trips.txt' 
INTO TABLE trips
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
