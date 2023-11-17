import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'


def table_exists(cursor, table_name):
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    table_name = "product"

    if not table_exists(cursor, table_name):
        cursor.execute('''
    CREATE TABLE product (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        manufactureDate TEXT,
        expiryDate TEXT,
        ratePerUnit REAL NOT NULL,
        unit TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        timeStamp TEXT,
        categoryId INTEGER NOT NULL,
        FOREIGN KEY (categoryId) REFERENCES category(id)
    )
''')
        conn.commit()
        conn.close()


def create_manager_creds():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    hashed_password = generate_password_hash("password", method='pbkdf2:sha1')

    cursor.execute(
        'INSERT INTO user (username, password, role) VALUES (?, ?, ?)',
        ('blacky', hashed_password, 'MANAGER')
    )
    conn.commit()
    conn.close()

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

def main_function(key):
    if key == 'create_table':
        create_table()
    elif key == 'create_manager_creds':
        create_manager_creds()
    elif key == 'script':
        script()
    else:
        print("Invalid key. Please provide a valid key.")

# Example usage:
main_function('create_table')
# main_function('create_manager_creds')
# main_function('script')
