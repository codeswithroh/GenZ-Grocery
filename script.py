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

    table_name = "association"

    if not table_exists(cursor, table_name):
        cursor.execute('''
    CREATE TABLE association (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cartId INTEGER NOT NULL,
        productId INTEGER NOT NULL,
        FOREIGN KEY (cartId) REFERENCES cart(id),
        FOREIGN KEY (productId) REFERENCES product(id)
    )
''')
        conn.commit()
        conn.close()

def delete_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    table_name = "cart"

    cursor.execute('''
    DROP TABLE IF EXISTS {}
    
'''.format(table_name))
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

    cursor.execute(" select * from user where cartId=3 ")
    data = cursor.fetchall()
    print(data)
    conn.commit()
    conn.close()

def main_function(key):
    if key == 'create_table':
        create_table()
    elif key == 'create_manager_creds':
        create_manager_creds()
    elif key == 'delete_table':
        delete_table()
    elif key == 'script':
        script()
    else:
        print("Invalid key. Please provide a valid key.")

# Example usage:
main_function('create_table')
# main_function('create_manager_creds')
# main_function('script')
