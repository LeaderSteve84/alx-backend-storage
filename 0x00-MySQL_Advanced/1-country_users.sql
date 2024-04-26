-- SQL script that creates a table users following some requirements:
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT,
	email VARCHAR(225) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
	PRIMARY KEY (id)
);
