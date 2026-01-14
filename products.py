from database import get_connection
from tabulate import tabulate

def list_products():
    """Display all available products"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT product_id, name, price, stock FROM products ORDER BY product_id')
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        print("No products available.")
        return
    
    headers = ["Product ID", "Product Name", "Price ($)", "Stock"]
    print("\n" + "="*80)
    print("AVAILABLE PRODUCTS")
    print("="*80)
    print(tabulate(products, headers=headers, tablefmt="grid"))
    print()

def search_product(search_term):
    """Search for products by name or description"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '%' + search_term + '%'
    cursor.execute('''
        SELECT product_id, name, description, price, stock 
        FROM products 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY product_id
    ''', (query, query))
    
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        print(f"\nNo products found matching '{search_term}'")
        return
    
    headers = ["ID", "Name", "Description", "Price ($)", "Stock"]
    print("\n" + "="*80)
    print(f"SEARCH RESULTS FOR '{search_term}'")
    print("="*80)
    print(tabulate(products, headers=headers, tablefmt="grid", maxcolwidths=[3, 20, 30, 10, 7]))
    print()

def get_product_details(product_id):
    """Get detailed information about a specific product"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT product_id, name, description, price, stock, created_at
        FROM products 
        WHERE product_id = ?
    ''', (product_id,))
    
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        print(f"Product with ID {product_id} not found.")
        return None
    
    print("\n" + "="*80)
    print("PRODUCT DETAILS")
    print("="*80)
    print(f"Product ID:    {product[0]}")
    print(f"Name:          {product[1]}")
    print(f"Description:   {product[2]}")
    print(f"Price:         ${product[3]:.2f}")
    print(f"Stock:         {product[4]} units")
    print(f"Added:         {product[5]}")
    print("="*80 + "\n")
    
    return product

def check_product_stock(product_id, quantity):
    """Check if a product has sufficient stock"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT stock FROM products WHERE product_id = ?', (product_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False, "Product not found"
    
    stock = result[0]
    if stock < quantity:
        return False, f"Insufficient stock. Available: {stock}, Requested: {quantity}"
    
    return True, "Stock available"
