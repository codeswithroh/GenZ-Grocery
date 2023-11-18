from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functions.auth_function import create_user, signin_user
from functions.categories_function import create_category,get_categories,edit_category, delete_category
from functions.products_function import create_product, get_product,get_product_by_productId, edit_product, delete_product

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Change this to a secure secret key

# SQLite database configuration
DATABASE = 'database.db'

@app.context_processor
def set_authentication():
    user_authenticated = session.get('authenticated')
    return dict(authenticated=user_authenticated)

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
def signin(role="USER"):
    user_signed_in = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_signed_in = signin_user(username, password, role)

        if user_signed_in :
            session['authenticated'] = True
            session['role'] = role
            if role == 'MANAGER':
                return redirect(url_for('dashboard')) 
            else:
                return redirect(url_for('userDashboard'))
        else: 
            session['authenticated'] = False
            session.pop('role', None)

    return render_template('signin.html', role= role)

@app.route('/user', methods = ['GET','POST'])
def userDashboard():
    categories = []
    products = []
    if not session['authenticated']:
        return redirect(url_for('signin'))
    categories = get_categories()
    for categoryId,name in categories:
        product = get_product(categoryId)
        products.append(product)
    print(products)
    return render_template('userDashboard.html', categories = categories, products = products)

@app.route('/logout', methods=['GET','POST'])
def logout():
    print(session.get('authenticated'))
    if request.method == 'POST':
        session['authenticated'] = False
        session.pop('role', None)
        return redirect(url_for('signin'))

@app.route('/',methods=["GET","POST","PUT"])
def dashboard():
    categories=[]
    products=[]
    if session.get('authenticated'):
        role = session.get('role')
        if request.method == 'GET':
            categories= get_categories("")

            for categoryId,category in categories:
                product = get_product(categoryId)
                products.append(product)    
        if request.method == 'POST':
            return redirect(url_for('addCategories'))
        return render_template('dashboard.html', role=role, categories=categories, products = products)
    else:
        return redirect(url_for('signin'))

@app.route('/categories/add', methods=['GET','POST'])
def addCategories():
    if request.method == 'POST':
        name = request.form['name']
        category = create_category(name) 

        if category:
            return redirect(url_for('dashboard'))

    return render_template('categoryForm.html')

@app.route('/categories/edit/<name>', methods=['GET','POST'])
def editCategories(name=""):
    if request.method == "POST":
        newCategoryName = request.form['name']
        changedCategory = edit_category(name, newCategoryName)
        return redirect(url_for('dashboard'))

    return render_template('categoryForm.html', name=name)

@app.route('/categories/delete/<name>', methods=['GET','POST'])
def deleteCategories(name=""):
    if request.method == "GET":
        deleteCategory = delete_category(name)
    return redirect(url_for('dashboard'))

@app.route('/products/add/<categoryId>', methods=['GET','POST'])
def addProduct(categoryId=0):
    if request.method == "POST":
        name = request.form['name']
        unit = request.form['unit']
        ratePerUnit = request.form['ratePerUnit']
        quantity = request.form['quantity']

        product = create_product(name, unit, ratePerUnit, quantity, categoryId) 

        if product:
            return redirect(url_for('dashboard'))
    return render_template('productForm.html')

@app.route('/products/delete/<productId>', methods=['GET','POST'])
def deleteProduct(productId=0):
    if request.method == "GET":
        deleteCategory = delete_product(productId)
    return redirect(url_for('dashboard'))

@app.route('/products/edit/<productId>', methods=['GET','POST'])
def editProduct(productId=0):
    product= []
    if request.method == 'GET':
        product = get_product_by_productId(productId)
    if request.method == "POST":
        # product_id, new_name, new_rate_per_unit, new_unit, new_quantity
        name = request.form['name']
        ratePerUnit = request.form['ratePerUnit']
        unit = request.form['unit']
        quantity = request.form['quantity']
        changedCategory = edit_product(productId, name, ratePerUnit, unit, quantity)
        return redirect(url_for('dashboard'))

    return render_template('productForm.html', product = product, productId = productId)

@app.route("/<path:path>")
def not_found(path):
    return render_template('404.html'),404
        
if __name__ == '__main__':
    app.run(debug=True)


