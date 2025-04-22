DROP TABLE IF EXISTS users;

CREATE TABLE users (
    pvt_id SERIAL PRIMARY KEY,
    user_id BINARY(16) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(150) NOT NULL,
    password BLOB NOT NULL,
    password_salt BLOB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    last_logged_in TIMESTAMP
);