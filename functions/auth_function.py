import sqlite3
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"

def create_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('Username already exists', 'error')
        return False
    else:
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha1')

        # Insert user into the database
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        flash('Signup successful', 'success')
        
        return True

def signin_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username exists
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        # User authentication successful
        flash('Signin successful', 'success')
        return True
    else:
        flash('Invalid username or password', 'error')
        return False
