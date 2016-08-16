import sqlite3

from flask import Flask, g, render_template

import db_access

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/users')
def users():
    user_list = db_access.get_all_users()
    return render_template('admin/users.html', users=user_list)


@app.route('/admin/chirps')
def chirps():
    chirp_list = db_access.get_all_chirps()
    return render_template('admin/chirps.html', chirps=chirp_list)


if __name__ == '__main__':
    app.run(debug=True)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'conn'):
        g.conn.close()