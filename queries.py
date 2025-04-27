import sqlite3

DATABASE_NAME = 'store.db'

def add_product(name, category, price, stock_quantity):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)',
                   (name, category, price, stock_quantity))
    conn.commit()
    conn.close()

def add_customer(name, email):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Customers (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

def record_sale(customer_id, total_amount, sale_items):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Sales (customer_id, total_amount) VALUES (?, ?)', (customer_id, total_amount))
    sale_id = cursor.lastrowid

    for product_id, quantity in sale_items.items():
        cursor.execute('SELECT price FROM Products WHERE product_id = ?', (product_id,))
        price = cursor.fetchone()[0]
        cursor.execute('INSERT INTO Sale_Items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                       (sale_id, product_id, quantity, price))

    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Customers WHERE customer_id = ?', (customer_id,))
    conn.commit()
    conn.close()

def fetch_products():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, name, category, price, stock_quantity FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products

def fetch_customers():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT customer_id, name, email FROM Customers')
    customers = cursor.fetchall()
    conn.close()
    return customers