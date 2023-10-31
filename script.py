import sqlite3

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

# create_table()

def create_manager_creds():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
        ('pom','pom','MANAGER')
    )
    conn.commit()
    conn.close()

create_manager_creds()


def script():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    table_name = "user"
    
    
    cursor.execute(" SELECT * FROM user WHERE role = 'MANAGER'; ")
    table_names = cursor.fetchall()
    print(table_names)
    conn.commit()
    
    
    conn.close()

# script()

