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
INSERT INTO "chirp" VALUES(1,'Hello?',1,'2016-08-17 21:26:33.364727');
INSERT INTO "chirp" VALUES(2,'Is this thing on?',2,'2016-08-17 21:26:43.364727');
INSERT INTO "chirp" VALUES(3,'I saw that!',3,'2016-08-17 21:43:33.364727');
INSERT INTO "chirp" VALUES(4,'40 characters, limiting',1,'2016-08-17 23:26:33.364727');
INSERT INTO "chirp" VALUES(5,'I like pie',2,'2016-08-18 21:26:33.364727');
INSERT INTO "chirp" VALUES(6,'I like python',1,'2016-09-17 21:26:33.364727');
INSERT INTO "chirp" VALUES(7,'The web is sublime',3,'2016-09-17 21:26:33.364727');
INSERT INTO "chirp" VALUES(8,'Who is Tim Berners-Lee?',4,'2017-08-17 21:26:33.364727');
CREATE TABLE migration (
    script TEXT PRIMARY KEY
);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('user',6);
INSERT INTO "sqlite_sequence" VALUES('chirp',8);
COMMIT;
