import tkinter as tk
from tkinter import messagebox, ttk
from database import create_database, populate_database
from queries import add_product, add_customer, record_sale, delete_product, delete_customer, fetch_products, fetch_customers

# Создание базы данных и заполнение начальными данными
create_database()
populate_database()

# Создание GUI
app = tk.Tk()
app.title("Система учета товаров")

# --- Форма для добавления товара ---
product_frame = ttk.LabelFrame(app, text="Добавить товар")
product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(product_frame, text="Название товара").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Label(product_frame, text="Категория").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Label(product_frame, text="Цена").grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Label(product_frame, text="Количество").grid(row=3, column=0, padx=5, pady=5, sticky="w")

product_name_entry = ttk.Entry(product_frame)
product_category_entry = ttk.Entry(product_frame)
product_price_entry = ttk.Entry(product_frame)
product_quantity_entry = ttk.Entry(product_frame)

product_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
product_category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
product_price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
product_quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

def add_product_to_db():
    name = product_name_entry.get()
    category = product_category_entry.get()
    try:
        price = float(product_price_entry.get())
        stock_quantity = int(product_quantity_entry.get())
        add_product(name, category, price, stock_quantity)
        messagebox.showinfo("Успех", "Товар добавлен!")
        clear_product_fields()
        update_product_list()
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для цены и количества.")

ttk.Button(product_frame, text="Добавить товар", command=add_product_to_db).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_product_fields():
    product_name_entry.delete(0, tk.END)
    product_category_entry.delete(0, tk.END)
    product_price_entry.delete(0, tk.END)
    product_quantity_entry.delete(0, tk.END)

# --- Форма для добавления покупателя ---
customer_frame = ttk.LabelFrame(app, text="Добавить покупателя")
customer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

ttk.Label(customer_frame, text="Имя покупателя").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Label(customer_frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="w")

customer_name_entry = ttk.Entry(customer_frame)
customer_email_entry = ttk.Entry(customer_frame)

customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
customer_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

def add_customer_to_db():
    name = customer_name_entry.get()
    email = customer_email_entry.get()
    add_customer(name, email)
    messagebox.showinfo("Успех", "Покупатель добавлен!")
    clear_customer_fields()
    update_customer_list()

ttk.Button(customer_frame, text="Добавить покупателя", command=add_customer_to_db).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_customer_fields():
    customer_name_entry.delete(0, tk.END)
    customer_email_entry.delete(0, tk.END)

# --- Форма для записи продажи ---
sale_frame = ttk.LabelFrame(app, text="Записать продажу")
sale_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(sale_frame, text="ID покупателя").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Label(sale_frame, text="Общая сумма").grid(row=1, column=0, padx=5, pady=5, sticky="w")

sale_customer_id_entry = ttk.Entry(sale_frame)
sale_total_amount_entry = ttk.Entry(sale_frame)

sale_customer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
sale_total_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

sale_items = {1: 2, 2: 1}  # Пример

def record_sale_to_db():
    try:
        customer_id = int(sale_customer_id_entry.get())
        total_amount = float(sale_total_amount_entry.get())
        record_sale(customer_id, total_amount, sale_items)
        messagebox.showinfo("Успех", "Продажа записана!")
        clear_sale_fields()
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для ID покупателя и общей суммы.")

ttk.Button(sale_frame, text="Записать продажу", command=record_sale_to_db).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_sale_fields():
    sale_customer_id_entry.delete(0, tk.END)
    sale_total_amount_entry.delete(0, tk.END)

# --- Отображение товаров ---
products_list_frame = ttk.LabelFrame(app, text="Список товаров")
products_list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

products_tree = ttk.Treeview(products_list_frame, columns=("ID", "Название", "Категория", "Цена", "Количество"), show="headings")
products_tree.heading("ID", text="ID")
products_tree.heading("Название", text="Название")
products_tree.heading("Категория", text="Категория")
products_tree.heading("Цена", text="Цена")
products_tree.heading("Количество", text="Количество")
products_tree.pack(fill="both", expand=True)

def update_product_list():
    for item in products_tree.get_children():
        products_tree.delete(item)
    products = fetch_products()
    for product in products:
        products_tree.insert("", tk.END, values=product)

def delete_selected_product():
    selected_item = products_tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите товар для удаления.")
        return
    product_id = products_tree.item(selected_item[0])['values'][0]
    if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить товар с ID {product_id}?"):
        delete_product(product_id)
        messagebox.showinfo("Успех", "Товар удален!")
        update_product_list()

delete_product_button = ttk.Button(products_list_frame, text="Удалить товар", command=delete_selected_product)
delete_product_button.pack(pady=5, fill="x")

update_product_list()

# --- Отображение покупателей ---
customers_list_frame = ttk.LabelFrame(app, text="Список покупателей")
customers_list_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

customers_tree = ttk.Treeview(customers_list_frame, columns=("ID", "Имя", "Email"), show="headings")
customers_tree.heading("ID", text="ID")
customers_tree.heading("Имя", text="Имя")
customers_tree.heading("Email", text="Email")
customers_tree.pack(fill="both", expand=True)

def update_customer_list():
    for item in customers_tree.get_children():
        customers_tree.delete(item)
    customers = fetch_customers()
    for customer in customers:
        customers_tree.insert("", tk.END, values=customer)

def delete_selected_customer():
    selected_item = customers_tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите покупателя для удаления.")
        return
    customer_id = customers_tree.item(selected_item[0])['values'][0]
    if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить покупателя с ID {customer_id}?"):
        delete_customer(customer_id)
        messagebox.showinfo("Успех", "Покупатель удален!")
        update_customer_list()

delete_customer_button = ttk.Button(customers_list_frame, text="Удалить покупателя", command=delete_selected_customer)
delete_customer_button.pack(pady=5, fill="x")

update_customer_list()

# Настройка весов строк и столбцов для резинового изменения размера
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

app.mainloop()