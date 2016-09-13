from flask import Flask, request, g, render_template, redirect, url_for, flash, session
import os
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
    data = False
    error = None
    if (len(handle) < 20 and len(handle) > 1) == (False):
        error = 'Username is too %s.' % ('long' if len(handle) > 1 else 'short')
    elif (len(password) < 20 and len(password) > 4) == (False):
        error = 'Password is too %s.' % ('long' if len(password) > 1 else 'short')
    if error is None:
        data = db_access.create_account(handle, password)
    if data is False:
        flash(error, 'account_err')
        return redirect(url_for('account'))
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
    return redirect(url_for('index'))
    
app.secret_key = os.environ['SECRET_KEY']
if __name__ == '__main__':
    app.run(debug=True)
