import sqlite3

DATABASE = 'database.db'

def script():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    table_name = "user"
    
    
    cursor.execute('DROP TABLE IF EXISTS user')

    conn.commit()
    
    
    conn.close()

