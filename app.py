from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functions.auth_function import create_user, signin_user

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Change this to a secure secret key

# SQLite database configuration
DATABASE = 'database.db'

@app.context_processor
def set_authentication():
    user_authenticated = session.get('authenticated')
    return dict(authenticated=user_authenticated)

# Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_created = create_user(username, password)

        if user_created:
            return redirect(url_for('signin')) 

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])    
@app.route('/signin/<role>', methods=['GET', 'POST'])
def signin(role="USER"):
    user_signed_in = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_signed_in = signin_user(username, password, role)

        if user_signed_in :
            session['authenticated'] = True
            session['role'] = role
            return redirect(url_for('dashboard')) 
        else: 
            session['authenticated'] = False
            session.pop('role', None)

    return render_template('signin.html', role= role)

@app.route('/logout', methods=['GET','POST'])
def logout():
    print(session.get('authenticated'))
    if request.method == 'POST':
        session['authenticated'] = False
        session.pop('role', None)
        return redirect(url_for('signin'))

@app.route('/')
def dashboard():
    if session.get('authenticated'):
        role = session.get('role')
        return render_template('dashboard.html', role=role)
    else:
        return redirect(url_for('signin'))

@app.route("/<path:path>")
def not_found(path):
    return render_template('404.html'),404


        
if __name__ == '__main__':
    app.run(debug=True)


