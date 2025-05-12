import sqlite3

DATABASE_NAME = 'store.db'
INITIAL_DATA_FILE = 'initial_data.txt'

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sale_Items (
        sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES Sales(sale_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )''')

    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        with open(INITIAL_DATA_FILE, 'r', encoding='utf-8') as f:
            current_table = None
            columns = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == 'PRODUCTS':
                    current_table = 'Products'
                    columns = []
                elif line == 'CUSTOMERS':
                    current_table = 'Customers'
                    columns = []
                elif current_table and not columns:
                    columns = [col.strip() for col in line.split(',')]
                elif current_table and columns:
                    values = [val.strip() for val in line.split(',')]
                    if current_table == 'Products' and len(columns) == 4 and len(values) == 4:
                        cursor.execute('SELECT 1 FROM Products WHERE name = ?', (values[0],))
                        if not cursor.fetchone():
                            cursor.execute(
                                'INSERT INTO Products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)',
                                (values[0], values[1], float(values[2]), int(values[3]))
                            )
                    elif current_table == 'Customers' and len(columns) == 2 and len(values) == 2:
                        # Check if customer already exists
                        cursor.execute('SELECT 1 FROM Customers WHERE email = ?', (values[1],))
                        if not cursor.fetchone():
                            cursor.execute(
                                'INSERT INTO Customers (name, email) VALUES (?, ?)',
                                (values[0], values[1])
                            )
        conn.commit()
    except FileNotFoundError:
        print(f"Warning: File '{INITIAL_DATA_FILE}' not found. Skipping initial data population.")
    except Exception as e:
        print(f"Error populating database from '{INITIAL_DATA_FILE}': {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
    populate_database()
    print(f"Database '{DATABASE_NAME}' created and populated (if '{INITIAL_DATA_FILE}' exists).")