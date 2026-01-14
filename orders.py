from database import get_connection
from tabulate import tabulate
from datetime import datetime

def create_order(customer_name, customer_email, shipping_address):
    """Create an order from the current cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get cart items
    cursor.execute('''
        SELECT c.product_id, p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
    ''')
    
    cart_items = cursor.fetchall()
    
    if not cart_items:
        print("Error: Cannot create order with empty cart.")
        conn.close()
        return False
    
    # Calculate total
    total_amount = sum(price * quantity for _, _, price, quantity in cart_items)
    
    try:
        # Insert order
        cursor.execute('''
            INSERT INTO orders (customer_name, customer_email, shipping_address, total_amount)
            VALUES (?, ?, ?, ?)
        ''', (customer_name, customer_email, shipping_address, total_amount))
        
        order_id = cursor.lastrowid
        
        # Insert order items and update product stock
        for product_id, name, price, quantity in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, product_id, quantity, price))
            
            # Update product stock
            cursor.execute('''
                UPDATE products
                SET stock = stock - ?
                WHERE product_id = ?
            ''', (quantity, product_id))
        
        # Clear cart
        cursor.execute('DELETE FROM cart')
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*80)
        print("ORDER CONFIRMATION")
        print("="*80)
        print(f"Order ID:          #{order_id}")
        print(f"Customer Name:     {customer_name}")
        print(f"Email:             {customer_email}")
        print(f"Shipping Address:  {shipping_address}")
        print(f"Order Date:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Amount:      ${total_amount:.2f}")
        print(f"Status:            Pending")
        print("="*80)
        print("✓ Order created successfully! Your cart has been cleared.\n")
        
        return True
    
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error creating order: {str(e)}")
        return False

def list_orders():
    """Display all orders"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT order_id, customer_name, total_amount, status, order_date
        FROM orders
        ORDER BY order_date DESC
    ''')
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        print("\n" + "="*80)
        print("ORDER HISTORY")
        print("="*80)
        print("No orders found.")
        print()
        return
    
    print("\n" + "="*80)
    print("ORDER HISTORY")
    print("="*80)
    
    display_orders = []
    for order in orders:
        display_orders.append([order[0], order[1], f"${order[2]:.2f}", order[3], order[4]])
    
    headers = ["Order ID", "Customer Name", "Total ($)", "Status", "Date"]
    print(tabulate(display_orders, headers=headers, tablefmt="grid"))
    print()

def get_order_details(order_id):
    """Get detailed information about a specific order"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get order header
    cursor.execute('''
        SELECT order_id, customer_name, customer_email, shipping_address, 
               total_amount, status, order_date
        FROM orders
        WHERE order_id = ?
    ''', (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        print(f"Error: Order with ID {order_id} not found.")
        conn.close()
        return
    
    # Get order items
    cursor.execute('''
        SELECT oi.product_id, p.name, oi.quantity, oi.unit_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    ''', (order_id,))
    
    items = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*80)
    print(f"ORDER DETAILS - Order #{order[0]}")
    print("="*80)
    print(f"Customer Name:     {order[1]}")
    print(f"Email:             {order[2]}")
    print(f"Shipping Address:  {order[3]}")
    print(f"Order Date:        {order[6]}")
    print(f"Status:            {order[5]}")
    print("-"*80)
    
    display_items = []
    for item in items:
        item_total = item[2] * item[3]
        display_items.append([item[1], item[2], f"${item[3]:.2f}", f"${item_total:.2f}"])
    
    headers = ["Product Name", "Quantity", "Unit Price", "Total"]
    print(tabulate(display_items, headers=headers, tablefmt="grid"))
    
    print("-"*80)
    print(f"{'Total Amount:':<50} ${order[4]:.2f}")
    print("="*80 + "\n")

def track_order(order_id):
    """Track the status of an order"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT order_id, customer_name, status, order_date, total_amount
        FROM orders
        WHERE order_id = ?
    ''', (order_id,))
    
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        print(f"Error: Order with ID {order_id} not found.")
        return
    
    print("\n" + "="*80)
    print("ORDER TRACKING")
    print("="*80)
    print(f"Order ID:     #{order[0]}")
    print(f"Customer:     {order[1]}")
    print(f"Order Date:   {order[3]}")
    print(f"Amount:       ${order[4]:.2f}")
    print("-"*80)
    print(f"Current Status: {order[2]}")
    
    # Show status timeline
    statuses = ["Pending", "Processing", "Shipped", "Delivered"]
    current_status = order[2]
    
    print("\nStatus Timeline:")
    for status in statuses:
        if status == current_status:
            print(f"  ✓ {status} (Current)")
        elif statuses.index(status) < statuses.index(current_status):
            print(f"  ✓ {status} (Completed)")
        else:
            print(f"  ○ {status} (Pending)")
    
    print("="*80 + "\n")

def update_order_status(order_id, new_status):
    """Update the status of an order"""
    valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    
    if new_status not in valid_statuses:
        print(f"Error: Invalid status. Valid statuses are: {', '.join(valid_statuses)}")
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT order_id FROM orders WHERE order_id = ?', (order_id,))
    if not cursor.fetchone():
        print(f"Error: Order with ID {order_id} not found.")
        conn.close()
        return False
    
    cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', (new_status, order_id))
    conn.commit()
    conn.close()
    
    print(f"✓ Order #{order_id} status updated to '{new_status}'")
    return True

def search_orders_by_customer(customer_name):
    """Search for orders by customer name"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '%' + customer_name + '%'
    cursor.execute('''
        SELECT order_id, customer_name, total_amount, status, order_date
        FROM orders
        WHERE customer_name LIKE ?
        ORDER BY order_date DESC
    ''', (query,))
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        print(f"\nNo orders found for customer '{customer_name}'")
        return
    
    print("\n" + "="*80)
    print(f"ORDERS FOR '{customer_name}'")
    print("="*80)
    
    display_orders = []
    for order in orders:
        display_orders.append([order[0], order[1], f"${order[2]:.2f}", order[3], order[4]])
    
    headers = ["Order ID", "Customer Name", "Total ($)", "Status", "Date"]
    print(tabulate(display_orders, headers=headers, tablefmt="grid"))
    print()
