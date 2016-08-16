import sqlite3


def get_all():
    conn = sqlite3.connect('data/chirpr.db')
    rows = conn.execute('select id, handle from user').fetchall()
    return [{'id': row[0], 'handle': row[1]} for row in rows]
