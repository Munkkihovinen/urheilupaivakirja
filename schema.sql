CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE activities (
    id INTEGER PRIMARY KEY,
    sent_at TEXT,
    sport TEXT,
    duration_in_minutes  INTEGER,
    content TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    activity_id INTEGER REFERENCES activities
);