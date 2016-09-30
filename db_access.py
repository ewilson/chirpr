import sqlite3
import datetime, hashlib
from flask import app, g

from chirpr import app

def hash_ps(text):
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def get_all_chirps(uid):
    conn = get_db()
    return conn.execute('SELECT c.id, c.body, c.datetime, u.handle FROM chirp c, user u WHERE c.user_id = u.id ORDER BY c.id DESC').fetchall()


def delete_chirp(chirp_id, user_id):
    conn = get_db()
    conn.execute('DELETE FROM chirp WHERE id = :id', {'id': chirp_id})
    conn.commit()
    

def get_all_users():
    conn = get_db()
    return conn.execute('SELECT id, handle, admin FROM user').fetchall()


def follower_of(leader_id, follower_id):
    conn = get_db()
    return conn.execute('SELECT * FROM followers WHERE leader_id=:lid AND follower_id=:fid', {'lid':leader_id, 'fid':follower_id}).fetchone()


def follow(leader_id, follower_id):
    conn = get_db()
    if follower_of(leader_id, follower_id) is None:
        conn.execute('INSERT INTO followers VALUES (?,?)', (leader_id, follower_id))
        conn.commit()
        return True
    return False


def followers(uid):
    conn = get_db()
    return conn.execute('SELECT leader_id FROM followers WHERE follower_id=?', (uid,)).fetchall()


def follow_data(leader_id):
    conn = get_db()
    followers = {'count_followers':0}
    f = 'count_followers'
    for i in conn.execute('SELECT leader_id, follower_id FROM followers WHERE leader_id=?', (leader_id,)):
        if f in followers:
            followers[f] += 1
    return followers


def get_user(uid):
    conn = get_db()
    user = conn.execute('SELECT handle FROM user WHERE id=:id', {'id':uid}).fetchone()
    return user[0] if user is not None else None
    

def get_id(user):
    conn = get_db()
    ID = conn.execute('SELECT id FROM user WHERE handle=:user', {'user':user}).fetchone()
    return ID[0] if ID is not None else None


def get_users_like(like_handle):
    conn = get_db()
    like_handle = '%' + like_handle + '%'
    return list(conn.execute('SELECT * FROM user WHERE handle LIKE :like_handle', {'like_handle':like_handle}))
   
    
def get_user_by_handle_and_password(handle, password):
    conn = get_db()
    password = hash_ps(password)
    return conn.execute('SELECT id FROM user WHERE handle=:handle AND password=:password', {'handle':handle, 'password':password}).fetchone()
    
    
def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM user WHERE id = :id', {'id': user_id})
    conn.commit()


def add_user(handle, password):
    password = hash_ps(password)
    conn = get_db()
    conn.execute('INSERT INTO user (handle, password, admin) values (:handle, :password, :admin)',
                 {'handle': handle, 'password':password, 'admin': 0})
    conn.commit()


def create_account(handle, password):
    conn = get_db()
    res = conn.execute('SELECT * FROM user WHERE handle=:handle', {'handle':handle})
    if list(res):
        state = False
    else:
        add_user(handle, password)
        state = True
    return state


def get_db():
    if not hasattr(g, 'chirpr.db'):
        g.conn = connect_db()
    return g.conn


def connect_db():
    conn = sqlite3.connect('data/chirpr.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'conn'):
        g.conn.close()
