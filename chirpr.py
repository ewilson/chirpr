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


@app.route('/admin/user/add', methods=['POST'])
def add_user():
    handle = request.form.get('handle')
    db_access.add_user(handle)
    return redirect(url_for('users'))


@app.route('/admin/chirps')
def chirps():
    chirp_list = db_access.get_all_chirps()
    return render_template('admin/chirps.html', chirps=chirp_list)

@app.route('/chirp', methods=['GET', 'POST'])
def chirp():
    if request.method == 'POST':
        ID = db_access.add_chirp(request.form["content"])
    chirp_list = db_access.get_all_chirps()
    return render_template('chirp.html', chirps=chirp_list)
@app.route('/admin/chirp/delete/<chirp_id>')
def delete_chirp(chirp_id):
    db_access.delete_chirp(chirp_id)
    return redirect(url_for('chirps'))


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
if __name__ == '__main__':
    app.run(debug=True)
