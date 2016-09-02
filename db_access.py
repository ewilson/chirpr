import sqlite3
import datetime, hashlib
from flask import app, g

from chirpr import app

def hash_ps(text):
    t = hashlib.sha224()
    t.update(text.encode('utf-8'))
    t = t.hexdigest()
    return t


def get_all_chirps(uid):
    conn = get_db()
    chirps = []
    for text in conn.execute('SELECT c.id, c.body, c.datetime, u.handle FROM chirp c, user u, followers f WHERE f.handleid = ? AND c.user_id = u.id AND c.user_id = f.followerid ORDER BY c.id', (uid,)):
        chirps.append(text)
    return reversed(chirps)


def delete_chirp(chirp_id, user_id):
    conn = get_db()
    conn.execute('DELETE FROM chirp WHERE id = :id AND user_id = :uid', {'id': chirp_id, 'uid':user_id})
    conn.commit()


def get_all_users():
    conn = get_db()
    return conn.execute('SELECT id, handle, admin FROM user').fetchall()


def user_for(uid):
    conn = get_db()
    for a in conn.execute('SELECT handle FROM user WHERE id=:id', {'id':uid}):
        return a[0]
    return ''

def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM user WHERE id = :id', {'id': user_id})
    conn.commit()


def add_user(handle, password):
    password = hash_ps(password)
    conn = get_db()
    for c in conn.execute('SELECT * FROM user WHERE handle=:handle', {'handle':handle}):
        return list(c)
    conn.execute('INSERT INTO user (handle, password, admin) values (:handle, :password, :admin)',
                 {'handle': handle, 'password':password, 'admin': 0})
    conn.commit()


def get_db():
    if not hasattr(g, 'chirpr.db'):
        g.conn = connect_db()
    return g.conn


def connect_db():
    conn = sqlite3.connect('data/chirpr.db')
    conn.row_factory = sqlite3.Row
    return conn


def sign_in(handle, password):
    conn = get_db()
    password = hash_ps(password)
    for c in conn.execute('SELECT id FROM user WHERE handle=:handle AND password=:password', {'handle':handle, 'password':password}):
        return (True, c[0])
    return (False, -1)
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'conn'):
        g.conn.close()
