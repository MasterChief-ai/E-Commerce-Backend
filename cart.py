from database import get_connection
from tabulate import tabulate

def add_to_cart(product_id, quantity):
    """Add a product to the shopping cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if product exists
    cursor.execute('SELECT name, price, stock FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        print(f"Error: Product with ID {product_id} not found.")
        conn.close()
        return False
    
    name, price, stock = product
    
    if stock < quantity:
        print(f"Error: Insufficient stock. Available: {stock}, Requested: {quantity}")
        conn.close()
        return False
    
    # Check if product already in cart
    cursor.execute('SELECT cart_item_id, quantity FROM cart WHERE product_id = ?', (product_id,))
    cart_item = cursor.fetchone()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item[1] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE product_id = ?', (new_quantity, product_id))
        print(f"✓ Updated {name} quantity in cart to {new_quantity}")
    else:
        # Add new item to cart
        cursor.execute('''
            INSERT INTO cart (product_id, quantity)
            VALUES (?, ?)
        ''', (product_id, quantity))
        print(f"✓ Added {quantity}x {name} to cart (${price:.2f} each)")
    
    conn.commit()
    conn.close()
    return True

def view_cart():
    """Display the shopping cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.cart_item_id, c.product_id, p.name, p.price, c.quantity, c.added_at
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        ORDER BY c.added_at
    ''')
    
    cart_items = cursor.fetchall()
    conn.close()
    
    if not cart_items:
        print("\n" + "="*80)
        print("YOUR SHOPPING CART")
        print("="*80)
        print("Cart is empty.")
        print()
        return []
    
    print("\n" + "="*80)
    print("YOUR SHOPPING CART")
    print("="*80)
    
    display_items = []
    total = 0
    for item in cart_items:
        cart_id, product_id, name, price, quantity, added_at = item
        item_total = price * quantity
        total += item_total
        display_items.append([cart_id, product_id, name, quantity, f"${price:.2f}", f"${item_total:.2f}"])
    
    headers = ["Cart ID", "Product ID", "Product Name", "Quantity", "Unit Price", "Total"]
    print(tabulate(display_items, headers=headers, tablefmt="grid"))
    print(f"\n{'Subtotal:':<50} ${total:.2f}")
    print(f"{'Estimated Tax (10%):':<50} ${total * 0.10:.2f}")
    print(f"{'TOTAL:':<50} ${total * 1.10:.2f}")
    print("="*80 + "\n")
    
    return cart_items

def remove_from_cart(cart_item_id):
    """Remove an item from the cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get item details
    cursor.execute('''
        SELECT p.name FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.cart_item_id = ?
    ''', (cart_item_id,))
    
    result = cursor.fetchone()
    
    if not result:
        print(f"Error: Cart item with ID {cart_item_id} not found.")
        conn.close()
        return False
    
    name = result[0]
    
    cursor.execute('DELETE FROM cart WHERE cart_item_id = ?', (cart_item_id,))
    conn.commit()
    conn.close()
    
    print(f"✓ Removed {name} from cart")
    return True

def update_cart_quantity(cart_item_id, new_quantity):
    """Update the quantity of an item in the cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if new_quantity <= 0:
        print("Error: Quantity must be greater than 0.")
        conn.close()
        return False
    
    # Get product info
    cursor.execute('''
        SELECT p.name, p.stock FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.cart_item_id = ?
    ''', (cart_item_id,))
    
    result = cursor.fetchone()
    
    if not result:
        print(f"Error: Cart item with ID {cart_item_id} not found.")
        conn.close()
        return False
    
    name, stock = result
    
    if new_quantity > stock:
        print(f"Error: Insufficient stock. Available: {stock}, Requested: {new_quantity}")
        conn.close()
        return False
    
    cursor.execute('UPDATE cart SET quantity = ? WHERE cart_item_id = ?', (new_quantity, cart_item_id))
    conn.commit()
    conn.close()
    
    print(f"✓ Updated {name} quantity to {new_quantity}")
    return True

def clear_cart():
    """Clear all items from the cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()
    
    print("✓ Cart cleared")

def get_cart_total():
    """Calculate total cart value"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT SUM(p.price * c.quantity)
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if result[0] is None:
        return 0
    
    return result[0]
