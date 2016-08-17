#!/usr/local/bin/python3
#
# To reset from captured DB, run:
#
# ./init_db.py
#
# To reset to empty DB, run:
#
# ./init_db.py new
#
import os
from sys import argv
import sqlite3

SCHEMA_FILE = ''
DB_NAME = 'data/chirpr.db'

if os.path.isfile(DB_NAME):
    os.remove(DB_NAME)

if len(argv) > 1 and argv[1] == 'new':
    SCHEMA_FILE = 'data/schema.sql'
else:
    SCHEMA_FILE = 'data/test_chirpr.sql'

conn = sqlite3.connect(DB_NAME)
schema = open(SCHEMA_FILE).read()
conn.executescript(schema)
conn.commit()
