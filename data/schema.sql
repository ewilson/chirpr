CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT NOT NULL,
    admin INT
);

CREATE TABLE chirp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body TEXT NOT NULL,
    user_id INT,
    datetime TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE migration (
    script TEXT PRIMARY KEY
);
