CREATE DATABASE IF NOT EXISTS torchserve_db;

USE torchserve_db;

CREATE TABLE IF NOT EXISTS torchserve_log (
    id VARCHAR(255) PRIMARY KEY,
    request_time VARCHAR(255),
    ip VARCHAR(255),
    question TEXT,
    answer TEXT
);

# CREATE USER 'root'@'%' IDENTIFIED BY 'root';
# GRANT ALL PRIVILEGES ON torchserve_db.* TO 'root'@'%';
