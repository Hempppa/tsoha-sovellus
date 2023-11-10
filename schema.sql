DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friendlist;
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    deleted BOOLEAN
);
CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    area TEXT,
    starter TEXT,
    created_at TIMESTAMP,
    deleted BOOLEAN
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    writer TEXT,
    discussion TEXT,
    content TEXT,
    created_at TIMESTAMP,
    deleted BOOLEAN
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    passwords TEXT,
    admin BOOLEAN,
    deleted BOOLEAN
);
CREATE TABLE friendlist (
    id SERIAL PRIMARY KEY,
    user1 TEXt,
    user2 TEXT,
    UNIQUE (user1, user2),
    deleted BOOLEAN
);
INSERT INTO areas (names) VALUES ('Yleinen chatti');