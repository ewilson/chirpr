-- GENERATED SQL DUMP -- DO NOT MODIFY -- WILL BE OVERWRITTEN
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT NOT NULL,
    admin INT
);
INSERT INTO "user" VALUES(1,'daniel',0);
INSERT INTO "user" VALUES(2,'dalton',0);
INSERT INTO "user" VALUES(3,'preston',0);
INSERT INTO "user" VALUES(4,'grant',0);
INSERT INTO "user" VALUES(5,'wilsonericn',0);
INSERT INTO "user" VALUES(6,'admin',1);
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
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('user',6);
COMMIT;
