#!/usr/local/bin/python3
#
# Applies all new migration scripts to DB
#
import os
import sqlite3

filenames = [fn for fn in os.listdir('data/migrations') if fn.endswith('.sql')]
conn = sqlite3.connect('data/chirpr.db')

executed_scripts = conn.execute('SELECT script FROM migration').fetchall()
ex_script_names = [r[0] for r in executed_scripts]

for f in sorted(filenames):
    if f not in ex_script_names:
        print('EXECUTING MIGRATION SCRIPT: {0}'.format(f))
        sql = open('data/migrations/{0}'.format(f)).read()
        try:
            conn.executescript(sql)
            conn.execute('INSERT INTO migration VALUES (?)', (f,))
            conn.commit()
        except sqlite3.OperationalError as oe:
            print('Failure to execute {0}: {1}'.format(f, oe))
            conn.rollback()
            exit(1)
    else:
        print('SKIPPING MIGRATION SCRIPT: {0}'.format(f))
