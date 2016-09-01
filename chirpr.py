from flask import Flask, request, g, render_template, redirect, url_for, session

import db_access

app = Flask(__name__)
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('chirp'))
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
    tup = db_access.sign_in(handle, password)
    if tup[0] == True:
        session['user'] = tup[1]
    return redirect(url_for('users'))
  

@app.route('/account')
def account():
    return render_template('account.html')
 

@app.route('/user/following')
def following():
    return render_template('following.html')


@app.route('/user/login', methods=['POST'])
def login():
    handle = request.form.get('handle')
    password = request.form.get('password')
    #db_access.add_user(handle, password)
    tup = db_access.sign_in(handle, password)
    if tup[0] == True:
        session['user'] = tup[1]
        session['name'] = db_access.user_for(tup[1])
        return redirect(url_for('chirp'))
    return redirect(url_for('account', success='login0'))
    
    
@app.route('/user/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('account'))


@app.route('/admin/chirps')
def chirps():
    chirp_list = db_access.get_all_chirps()
    return render_template('admin/chirps.html', chirps=chirp_list)


@app.route('/chirp', methods=['GET', 'POST'])
def chirp():
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            ID = db_access.add_chirp(request.form["content"],user)
        chirp_list = db_access.get_all_chirps(user)
        return render_template('chirp.html', chirps=chirp_list, name=db_access.user_for(session['user']))
    return redirect(url_for('index'))
    
    
@app.route('/chirp/delete/<chirp_id>')
def delete_chirp(chirp_id):
    if 'user' in session:
        db_access.delete_chirp(chirp_id, session['user'])
        return redirect(url_for('chirp'))
    return redirect(url_for('index'))
    

@app.errorhandler(404)
def page_not_found(error):
    try:
        temp = list(request.path)
        del temp[0]
        temp = ''.join(temp) + '.html'
        if temp not in ['base.html', 'index.html', 'chirp.html']:
            text = render_template(temp)
        else:
            kill()
    except:
        text = render_template("404.html")
    return text
app.secret_key = open('SECRET_KEY~', 'r').read().replace('\n', '')
if __name__ == '__main__':
    app.run(debug=True)
