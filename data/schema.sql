CREATE TABLE user (
    id INT PRIMARY KEY,
    handle TEXT NOT NULL,
    admin INT
);

CREATE TABLE chirp (
    id INT PRIMARY KEY,
    body TEXT NOT NULL,
    user_id INT,
    datetime TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE migration (
    script TEXT PRIMARY KEY
);
