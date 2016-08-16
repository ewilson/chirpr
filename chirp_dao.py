import sqlite3


def get_all():
    conn = sqlite3.connect('data/chirpr.db')

    rows = conn.execute('''
        select c.id, c.body, c.datetime, u.handle
        from chirp c, user u
        where c.user_id = u.id
    ''').fetchall()

    return [{'id': row[0],
             'body': row[1],
             'datetime': row[2],
             'handle': row[3]} for row in rows]
