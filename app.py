from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functions.auth_function import create_user, signin_user

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Change this to a secure secret key

# SQLite database configuration
DATABASE = 'database.db'

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    table_name = "user"
    
    if not table_exists(cursor, table_name):
        cursor.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK (role IN ('USER', 'MANAGER')) DEFAULT 'USER',
                cartId INTEGER
            )
        ''')
        conn.commit()
    
    conn.close()

create_table()

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
def signin(role="user"):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_signed_in = signin_user(username, password)

        if user_signed_in :
            return redirect(url_for('dashboard')) 

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard! This is a protected route."

if __name__ == '__main__':
    app.run(debug=True)


