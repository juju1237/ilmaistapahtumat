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

CREATE INDEX IF NOT EXISTS idx_events_user_id ON events (user_id);
CREATE INDEX IF NOT EXISTS idx_events_date ON events (date);
CREATE INDEX IF NOT EXISTS idx_events_id ON events (id);
CREATE INDEX IF NOT EXISTS idx_event_classes_event_id ON event_classes (event_id);
CREATE INDEX IF NOT EXISTS idx_comments_event_id ON comments (event_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments (user_id);
CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
