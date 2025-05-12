import tkinter as tk
from tkinter import messagebox, ttk
from database import create_database, populate_database
from queries import add_product, add_customer, record_sale, delete_product, delete_customer, fetch_products, fetch_customers, fetch_sales, fetch_sale_items

# Создание базы данных и заполнение начальными данными
create_database()
populate_database()

# Создание GUI
app = tk.Tk()
app.title("Система учета товаров")
app.geometry("1000x700") # Установим начальный размер окна

# --- Создание вкладок ---
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# --- Вкладка "Добавление" ---
add_tab = ttk.Frame(notebook)
notebook.add(add_tab, text="Добавление")

# --- Форма для добавления товара (вкладка "Добавление") ---
product_frame = ttk.LabelFrame(add_tab, text="Добавить товар")
product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

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
        if not name or not category or price <= 0 or stock_quantity < 0:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля и введите корректные значения.")
            return
        add_product(name, category, price, stock_quantity)
        messagebox.showinfo("Успех", "Товар добавлен!")
        clear_product_fields()
        update_product_list() # Обновляем список товаров
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для цены и количества.")

ttk.Button(product_frame, text="Добавить товар", command=add_product_to_db).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_product_fields():
    product_name_entry.delete(0, tk.END)
    product_category_entry.delete(0, tk.END)
    product_price_entry.delete(0, tk.END)
    product_quantity_entry.delete(0, tk.END)

# --- Форма для добавления покупателя (вкладка "Добавление") ---
customer_frame = ttk.LabelFrame(add_tab, text="Добавить покупателя")
customer_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

ttk.Label(customer_frame, text="Имя покупателя").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Label(customer_frame, text="Email").grid(row=1, column=0, padx=5, pady=5, sticky="w")

customer_name_entry = ttk.Entry(customer_frame)
customer_email_entry = ttk.Entry(customer_frame)

customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
customer_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

def add_customer_to_db():
    name = customer_name_entry.get()
    email = customer_email_entry.get()
    if not name:
        messagebox.showerror("Ошибка", "Имя покупателя не может быть пустым.")
        return
    add_customer(name, email)
    messagebox.showinfo("Успех", "Покупатель добавлен!")
    clear_customer_fields()
    update_customer_list() # Обновляем список покупателей

ttk.Button(customer_frame, text="Добавить покупателя", command=add_customer_to_db).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_customer_fields():
    customer_name_entry.delete(0, tk.END)
    customer_email_entry.delete(0, tk.END)

# Настройка растягивания для add_tab
add_tab.grid_columnconfigure(0, weight=1)
add_tab.grid_columnconfigure(1, weight=1)
add_tab.grid_rowconfigure(0, weight=1)


# --- Вкладка "Продажи" ---
sales_tab = ttk.Frame(notebook)
notebook.add(sales_tab, text="Продажи")

# --- Форма для записи продажи (вкладка "Продажи") ---
sale_frame = ttk.LabelFrame(sales_tab, text="Записать продажу")
sale_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(sale_frame, text="ID покупателя").grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Label(sale_frame, text="Общая сумма").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Label(sale_frame, text="ID Продукта (кол-во)").grid(row=2, column=0, padx=5, pady=5, sticky="w") 

sale_customer_id_entry = ttk.Entry(sale_frame)
sale_total_amount_entry = ttk.Entry(sale_frame)
sale_items_entry = ttk.Entry(sale_frame) 

sale_customer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
sale_total_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
sale_items_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew") 

ttk.Label(sale_frame, text="Пример: 1:2, 3:1 (ID:Кол-во)").grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

def parse_sale_items(items_str):
    sale_items = {}
    if not items_str:
        return sale_items
    try:
        for item_pair in items_str.split(','):
            product_id_str, quantity_str = item_pair.strip().split(':')
            product_id = int(product_id_str.strip())
            quantity = int(quantity_str.strip())
            if product_id <= 0 or quantity <= 0:
                raise ValueError("ID продукта и количество должны быть положительными числами.")
            sale_items[product_id] = quantity
        return sale_items
    except Exception:
        raise ValueError("Неверный формат товаров. Используйте формат: ID:Кол-во, ID:Кол-во")

def record_sale_to_db():
    try:
        customer_id = int(sale_customer_id_entry.get())
        total_amount = float(sale_total_amount_entry.get())
        items_str = sale_items_entry.get()
        sale_items = parse_sale_items(items_str)

        if customer_id <= 0 or total_amount <= 0:
            messagebox.showerror("Ошибка", "ID покупателя и общая сумма должны быть положительными числами.")
            return
        if not sale_items:
            messagebox.showerror("Ошибка", "Пожалуйста, укажите хотя бы один товар для продажи.")
            return

        record_sale(customer_id, total_amount, sale_items)
        messagebox.showinfo("Успех", "Продажа записана!")
        clear_sale_fields()
        update_sales_list() # Обновляем список продаж
    except ValueError as ve:
        messagebox.showerror("Ошибка", str(ve))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при записи продажи: {e}")

ttk.Button(sale_frame, text="Записать продажу", command=record_sale_to_db).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def clear_sale_fields():
    sale_customer_id_entry.delete(0, tk.END)
    sale_total_amount_entry.delete(0, tk.END)
    sale_items_entry.delete(0, tk.END)

# --- Отображение продаж (Чеков) (вкладка "Продажи") ---
sales_list_frame = ttk.LabelFrame(sales_tab, text="Список продаж (Чеки)")
sales_list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") 

sales_tree = ttk.Treeview(sales_list_frame, columns=("ID Продажи", "ID Покупателя", "Дата", "Сумма"), show="headings")
sales_tree.heading("ID Продажи", text="ID Продажи")
sales_tree.heading("ID Покупателя", text="ID Покупателя")
sales_tree.heading("Дата", text="Дата")
sales_tree.heading("Сумма", text="Сумма")
sales_tree.pack(fill="both", expand=True)

def update_sales_list():
    for item in sales_tree.get_children():
        sales_tree.delete(item)
    sales = fetch_sales()
    for sale in sales:
        sales_tree.insert("", tk.END, values=sale)

def show_sale_details():
    selected_item = sales_tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите продажу для просмотра деталей.")
        return

    sale_data = sales_tree.item(selected_item[0])['values']
    sale_id = sale_data[0]
    customer_id = sale_data[1]
    sale_date = sale_data[2]
    total_amount = sale_data[3]

    details_window = tk.Toplevel(app)
    details_window.title(f"Детали продажи #{sale_id}")

    ttk.Label(details_window, text=f"ID Продажи: {sale_id}").pack(padx=10, pady=5, anchor="w")
    ttk.Label(details_window, text=f"ID Покупателя: {customer_id}").pack(padx=10, pady=5, anchor="w")
    ttk.Label(details_window, text=f"Дата: {sale_date}").pack(padx=10, pady=5, anchor="w")
    ttk.Label(details_window, text=f"Общая сумма: {total_amount:.2f}").pack(padx=10, pady=5, anchor="w")

    ttk.Label(details_window, text="Товары в продаже:", font=("TkDefaultFont", 10, "bold")).pack(padx=10, pady=10, anchor="w")

    sale_items_tree = ttk.Treeview(details_window, columns=("ID Продукта", "Название", "Количество", "Цена за ед.", "Сумма"), show="headings")
    sale_items_tree.heading("ID Продукта", text="ID Продукта")
    sale_items_tree.heading("Название", text="Название")
    sale_items_tree.heading("Количество", text="Количество")
    sale_items_tree.heading("Цена за ед.", text="Цена за ед.")
    sale_items_tree.heading("Сумма", text="Сумма")
    sale_items_tree.pack(fill="both", expand=True, padx=10, pady=5)

    items = fetch_sale_items(sale_id)
    for item in items:
        product_id, product_name, quantity, price_at_sale = item
        item_total = quantity * price_at_sale
        sale_items_tree.insert("", tk.END, values=(product_id, product_name, quantity, f"{price_at_sale:.2f}", f"{item_total:.2f}"))

    vsb = ttk.Scrollbar(details_window, orient="vertical", command=sale_items_tree.yview)
    vsb.pack(side='right', fill='y')
    sale_items_tree.configure(yscrollcommand=vsb.set)

    details_window.grab_set() # Make the details window modal
    app.wait_window(details_window)

ttk.Button(sales_list_frame, text="Показать детали продажи", command=show_sale_details).pack(pady=5, fill="x")

# Настройка растягивания для sales_tab
sales_tab.grid_columnconfigure(0, weight=1)
sales_tab.grid_columnconfigure(1, weight=1)
sales_tab.grid_rowconfigure(0, weight=1)

# --- Вкладка "Товары" ---
products_tab = ttk.Frame(notebook)
notebook.add(products_tab, text="Товары")

# --- Отображение товаров (вкладка "Товары") ---
products_list_frame = ttk.LabelFrame(products_tab, text="Список товаров")
products_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

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


# --- Вкладка "Покупатели" ---
customers_tab = ttk.Frame(notebook)
notebook.add(customers_tab, text="Покупатели")

# --- Отображение покупателей (вкладка "Покупатели") ---
customers_list_frame = ttk.LabelFrame(customers_tab, text="Список покупателей")
customers_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

# --- Инициализация списков при запуске и переключении вкладок ---
def on_tab_change(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    if selected_tab == "Товары":
        update_product_list()
    elif selected_tab == "Покупатели":
        update_customer_list()
    elif selected_tab == "Продажи":
        update_sales_list()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# Первоначальное обновление всех списков
update_product_list()
update_customer_list()
update_sales_list()

app.mainloop()