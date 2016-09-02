from flask import Flask, request, g, render_template, redirect, url_for

import db_access

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/admin/users')
def users():
    user_list = db_access.get_all_users()
    return render_template('admin/users.html', users=user_list)


@app.route('/admin/user/delete/<user_id>')
def delete_user(user_id):
    db_access.delete_user(user_id)
    return redirect(url_for('users'))
 

@app.route('/user/add', methods=['POST'])
def add_user():
    handle = request.form.get('handle')
    password = request.form.get('password')
    data = db_access.add_user(handle, password)
    if data != None:
        return redirect(url_for('account', success='create0'))
    return redirect(url_for('users'))
  

@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/admin/chirps')
def chirps():
    chirp_list = db_access.get_all_chirps()
    return render_template('admin/chirps.html', chirps=chirp_list)
    
    
@app.route('/chirp/delete/<chirp_id>')
def delete_chirp(chirp_id):
    if 'user' in session:
        db_access.delete_chirp(chirp_id, session['user'])
        return redirect(url_for('chirp'))
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
