import sqlite3
from flask import flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"

def create_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    conn.commit()
    conn.close()

    if existing_user:
        flash('Username already exists', 'error')
        return False
    else:
        cart = cursor.execute("INSERT INTO cart DEFAULT VALUES")
        cartId = cursor.lastrowid
        hashed_password = generate_password_hash(password, method='pbkdf2:sha1')
        cursor.execute("INSERT INTO user (username, password, cartId) VALUES (?, ?, ?)", (username, hashed_password, cartId))
        conn.commit()
        conn.close()
        flash('Signup successful', 'success')
        return True

def signin_user(username, password, role):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the username exists
    cursor.execute("SELECT * FROM user WHERE username = ? AND role = ?;", (username, role))
    user = cursor.fetchone()

    conn.commit()
    conn.close()

    if user and check_password_hash(user[2], password):
        userId = user[0]
        cartId = user[4]
        flash('Signin successful', 'success')
        return {"userId": userId, "success":True, "cartId": cartId}
    else:
        flash('Invalid username or password', 'error')
        return {"success":False}



        