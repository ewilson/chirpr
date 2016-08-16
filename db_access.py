import sqlite3

from flask import app, g


def get_all_chirps():
    conn = get_db()
    return conn.execute('''
        select c.id, c.body, c.datetime, u.handle
        from chirp c, user u
        where c.user_id = u.id
    ''').fetchall()


def get_all_users():
    conn = get_db()
    return conn.execute('select id, handle from user').fetchall()


def get_db():
    if not hasattr(g, 'chirpr.db'):
        g.conn = connect_db()
    return g.conn


def connect_db():
    conn = sqlite3.connect('data/chirpr.db')
    conn.row_factory = sqlite3.Row
    return conn
