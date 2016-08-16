from flask import Flask, render_template

import user_dao, chirp_dao

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/users')
def users():
    user_list = user_dao.get_all()
    return render_template('admin/users.html', users=user_list)


@app.route('/admin/chirps')
def chirps():
    chirp_list = chirp_dao.get_all()
    return render_template('admin/chirps.html', chirps=chirp_list)

if __name__ == '__main__':
    app.run(debug=True)
