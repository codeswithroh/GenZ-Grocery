import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'


def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    table_name = "category"
    
    if not table_exists(cursor, table_name):
        cursor.execute('''
            CREATE TABLE category (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()
    
        conn.close()

# create_table()

def create_manager_creds():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    hashed_password = generate_password_hash("password", method='pbkdf2:sha1')

    cursor.execute(
        'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
        ('blacky', hashed_password,'MANAGER')
    )
    conn.commit()
    conn.close()

# create_manager_creds()


def script():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    table_name = "user"
    
    # " SELECT * FROM user "
    # " DELETE FROM user WHERE role = 'MANAGER' "

    cursor.execute(" SELECT * FROM user ")
    table_names = cursor.fetchall()
    print(table_names)
    conn.commit()
    
    
    conn.close()

# script()

