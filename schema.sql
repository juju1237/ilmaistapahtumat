CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    image BLOB,
    user_id INTEGER REFERENCES users
);

CREATE TABLE IF NOT EXISTS event_classes (
    id INTEGER PRIMARY KEY,
    event_id INETGER REFERENCRS events,
    title TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events,
    user_id INTEGER REFERENCES users,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
