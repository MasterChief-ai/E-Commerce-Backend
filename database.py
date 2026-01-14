import sqlite3
import os
from datetime import datetime

DATABASE_FILE = 'ecommerce.db'

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            shipping_address TEXT
        )
    ''')
    
    # Order items table (items in each order)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get a database connection"""
    return sqlite3.connect(DATABASE_FILE)

def add_sample_products():
    """Add sample products to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if products already exist
    cursor.execute('SELECT COUNT(*) FROM products')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_products = [
            ('Wireless Mouse', 'Ergonomic wireless mouse with 2.4GHz connection', 25.99, 50),
            ('USB-C Cable', 'High-speed USB-C charging and data cable (2m)', 12.99, 100),
            ('Mechanical Keyboard', 'RGB Mechanical keyboard with Cherry switches', 89.99, 30),
            ('Monitor Stand', 'Adjustable monitor stand with storage drawer', 34.99, 25),
            ('Laptop Cooling Pad', 'USB powered cooling pad for laptops', 29.99, 40),
            ('Webcam HD', '1080p Full HD webcam with auto-focus', 59.99, 20),
            ('USB Hub', '7-port USB 3.0 hub with fast charging', 39.99, 35),
            ('Screen Protector', 'Anti-glare screen protector for 27 inch monitors', 15.99, 60),
            ('Desk Lamp', 'LED desk lamp with adjustable brightness', 44.99, 15),
            ('Cable Organizer', 'Silicone cable management clips (5 pack)', 9.99, 80),
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, description, price, stock)
            VALUES (?, ?, ?, ?)
        ''', sample_products)
        
        conn.commit()
    
    conn.close()
