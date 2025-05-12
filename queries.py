import sqlite3

DATABASE_NAME = 'store.db'

# Функция для добавления нового товара в базу данных
def add_product(name, category, price, stock_quantity):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)',
                   (name, category, price, stock_quantity))
    conn.commit()
    conn.close()

# Функция для добавления нового покупателя в базу данных
def add_customer(name, email):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Customers (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

# Функция для записи новой продажи, включая обновление количества товаров на складе
def record_sale(customer_id, total_amount, sale_items):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Начинаем транзакцию для обеспечения атомарности операции
    conn.execute("BEGIN TRANSACTION")
    try:
        # Вставляем запись о новой продаже в таблицу Sales
        cursor.execute('INSERT INTO Sales (customer_id, total_amount) VALUES (?, ?)', (customer_id, total_amount))
        sale_id = cursor.lastrowid # Получаем ID только что вставленной продажи

        for product_id, quantity in sale_items.items():
            # Получаем цену и текущее количество товара на складе
            cursor.execute('SELECT price, stock_quantity FROM Products WHERE product_id = ?', (product_id,))
            product_info = cursor.fetchone()
            
            if product_info is None:
                raise ValueError(f"Продукт с ID {product_id} не найден.")
            
            product_price, current_stock = product_info
            
            # Проверяем достаточно ли товара на складе
            if current_stock < quantity:
                raise ValueError(f"Недостаточно товара на складе для продукта с ID {product_id}. В наличии: {current_stock}, Запрошено: {quantity}.")

            # Вставляем запись о позиции в чеке (товаре в продаже)
            cursor.execute('INSERT INTO Sale_Items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                           (sale_id, product_id, quantity, product_price))
            
            # Обновляем количество товара на складе
            cursor.execute('UPDATE Products SET stock_quantity = stock_quantity - ? WHERE product_id = ?',
                           (quantity, product_id))

        conn.commit() # Если все операции прошли успешно, фиксируем изменения
    except Exception as e:
        conn.rollback() # В случае ошибки откатываем все изменения транзакции
        raise e # Передаем исключение выше для обработки в интерфейсе
    finally:
        conn.close() # Закрываем соединение с базой данных

# Функция для удаления товара из базы данных по его ID
def delete_product(product_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

# Функция для удаления покупателя из базы данных по его ID
def delete_customer(customer_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Customers WHERE customer_id = ?', (customer_id,))
    conn.commit()
    conn.close()

# Функция для получения списка всех товаров из базы данных
def fetch_products():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, name, category, price, stock_quantity FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products

# Функция для получения списка всех покупателей из базы данных
def fetch_customers():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT customer_id, name, email FROM Customers')
    customers = cursor.fetchall()
    conn.close()
    return customers

# Функция для получения списка всех продаж (чеков) из базы данных
def fetch_sales():
    """Fetches all sales records."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Выбираем ID продажи, ID покупателя, форматированную дату и общую сумму, сортируя по дате
    cursor.execute('SELECT sale_id, customer_id, strftime("%Y-%m-%d %H:%M:%S", sale_date), total_amount FROM Sales ORDER BY sale_date DESC')
    sales = cursor.fetchall()
    conn.close()
    return sales

# Функция для получения списка товаров, входящих в конкретную продажу, по ее ID
def fetch_sale_items(sale_id):
    """Fetches items for a specific sale ID."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Объединяем таблицы Sale_Items и Products для получения названий товаров
    cursor.execute('''
        SELECT
            si.product_id,    -- ID продукта в позиции чека
            p.name,           -- Название продукта
            si.quantity,      -- Количество продукта в позиции чека
            si.price          -- Цена продукта на момент продажи
        FROM
            Sale_Items si
        JOIN
            Products p ON si.product_id = p.product_id
        WHERE
            si.sale_id = ?
    ''', (sale_id,))
    items = cursor.fetchall()
    conn.close()
    return items