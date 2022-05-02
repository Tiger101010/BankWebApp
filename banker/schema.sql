-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  balance NUMERIC(10,2)	DEFAULT 0 NOT NULL
);

insert into user (username,password,balance) VALUES ('admin','admin',10000);
