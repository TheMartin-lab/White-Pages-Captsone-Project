CREATE DATABASE IF NOT EXISTS capstone_news_db;
CREATE OR REPLACE USER 'django_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON capstone_news_db.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
