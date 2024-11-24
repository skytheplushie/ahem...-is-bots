import sqlite3

connection = sqlite3.connect('crud_functions.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
''')

def get_all_products(product_id, title, description, price):
    