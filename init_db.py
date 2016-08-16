#!/usr/local/bin/python3

import sqlite3

conn = sqlite3.connect('data/chirpr.db')
schema = open('data/schema.sql').read()
conn.executescript(schema)

