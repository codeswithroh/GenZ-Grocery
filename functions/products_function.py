import sqlite3
from flask import flash

DATABASE = 'database.db'

def get_product(categoryId):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE categoryId = ?",(categoryId,))
    products = cursor.fetchall()
    return products

def get_product_by_productId(productId):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product WHERE id = ?",(productId,))
    product = cursor.fetchall()
    return product

def edit_product(product_id, new_name, new_rate_per_unit, new_unit, new_quantity):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if the new name already exists in the category
    cursor.execute("SELECT * FROM product WHERE name=?", (new_name,))
    category_exists = cursor.fetchall()

    if category_exists:
        flash("Product already exists", 'error')
        return False
    else:
        cursor.execute('''
            UPDATE product 
            SET 
                name=?, 
                ratePerUnit=?, 
                unit=?, 
                quantity=?
            WHERE id=?
        ''', (new_name, new_rate_per_unit, new_unit, new_quantity, product_id))

        conn.commit()
        conn.close()

        flash('Product edited successfully', 'success')
        return True

def delete_product(productId):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id=?",(productId,))
    conn.commit()
    conn.close()

    flash('Product deleted successfully','success')
    return True
        

def create_product(name, unit, ratePerUnit, quantity, categoryId):
    conn =sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # check if category already exits
    cursor.execute("SELECT * FROM product WHERE name = ?",(name,))
    existing_category = cursor.fetchone()

    if existing_category:
        flash('Product already exists','error')
        return False
    else:
        cursor.execute("INSERT INTO product (name, unit, ratePerUnit, quantity, categoryId) VALUES (?,?,?,?,?)",(name,unit,ratePerUnit,quantity, categoryId))
        conn.commit()
        conn.close()
        flash('Product added successfully','success')
        return True