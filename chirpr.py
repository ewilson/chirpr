from flask import Flask, request, g, render_template, redirect, url_for, flash, session, Response
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
    if len(handle) not in range(1,20):
        error = 'Username is too %s. Sorry for the inconvenience.' % ('long' if len(handle) > 1 else 'short')
    elif len(password) not in range(4,20):
        error = 'Your password must be equal to or greater than 4 and less then or equal too 20. (too %s)' % ('long' if len(password) > 1 else 'short')
    if error is None:
        error = 'Username already exists, not created.'
        data = db_access.create_account(handle, password)
    if data is False:
        flash(error, 'danger_message')
        return redirect(url_for('account'))
    login(handle, password) 
    return redirect(url_for('users'))
  

@app.route('/follow/<uid>')
def follow_user(uid):
    if 'user' in session:
        user = db_access.get_user(uid)
        message = ('Sorry, you cannot follow %s.' % (user), 'danger_message')
        if db_access.follow(uid, session['user']) == True:
            message = ('You are now following %s' %(user), 'success_message')
        flash(*message)
        return redirect(url_for('index'))
    return redirect(url_for('account'))
  

def get_followers():
    followers = db_access.followers(session['user'])
    return [f[0] for f in followers]
    

def login(handle, password):
    login_info = db_access.get_user_by_handle_and_password(handle, password)
    if login_info is not None:
        uid = login_info[0] # uid for user id
        handle = db_access.get_user(uid)
        session['user'] = uid
        session['name'] = handle
        flash('Hello %s!'%(handle),'success_message')
        return True
    return False
    
    
@app.route('/user/login', methods=['POST'])
def login_page():
    handle = request.form.get('handle')
    password = request.form.get('password')
    if login(handle, password) == True:
        return redirect(url_for('index'))
    flash('Sorry, these cridentials seem to be invalid. Not Signed-In', 'danger_message')
    return redirect(url_for('account'))


@app.route('/user/page/<handle>')
def user_page(handle):
    uid = db_access.get_id(handle)
    my_followers = []
    if 'user' in session:
        my_followers = get_followers()
    return render_template('user_page.html', handle=handle, uid=uid, follow_data=db_access.follow_data(uid), my_followers=my_followers, get_user=db_access.get_user)
    
    
@app.route('/search', methods=["POST", 'GET'])
def search():
    if request.method == 'POST':
        q = request.form.get('q')   
    else:
        q = request.args.get('q')
        q = '' if not q else q
    res = db_access.get_users_like(q)
    my_followers = []
    if 'user' in session:
        my_followers = get_followers()
    return render_template('search.html', result=res, qfill=q, my_followers=my_followers)
    
    
@app.route('/user/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('account'))
    
    
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
    app.run(debug=True, host='0.0.0.0')
