import sqlite3
from flask import flash

DATABASE = 'database.db'

def get_categories(name=""):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if name:
        cursor.execute("SELECT * FROM category WHERE name = ?",(name,))
    else:
        cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    return categories

def edit_category(oldName, newName):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM category WHERE name=?",(newName,))
    categoryExists = cursor.fetchall()

    if categoryExists:
        flash("Category already exists",'error')
        return False
    else:
        cursor.execute("UPDATE category SET name=? WHERE name=?",(newName,oldName))
        conn.commit()
        conn.close()

        flash('Category added successfully','success')
        return True

def delete_category(name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM category WHERE name=?",(name,))
    conn.commit()
    conn.close()

    flash('Category deleted successfully','success')
    return True
        

def create_category(name):
    conn =sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # check if category already exits
    cursor.execute("SELECT * FROM category WHERE name = ?",(name,))
    existing_category = cursor.fetchone()

    if existing_category:
        flash('Category already exists','error')
        return False
    else:
        cursor.execute("INSERT INTO category (name) VALUES (?)",(name,))
        conn.commit()
        conn.close()
        flash('Category added successfully','success')
        return True