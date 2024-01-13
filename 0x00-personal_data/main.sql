-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS radiant@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO 'radiant'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");
