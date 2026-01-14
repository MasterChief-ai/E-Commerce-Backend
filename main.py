"""
E-Commerce Backend System
A command-line based e-commerce application with product listing, shopping cart, and order tracking.
"""

import sys
from database import init_database, add_sample_products, get_connection
from products import list_products, search_product, get_product_details
from cart import add_to_cart, view_cart, remove_from_cart, update_cart_quantity, clear_cart, get_cart_total
from orders import create_order, list_orders, get_order_details, track_order, update_order_status, search_orders_by_customer

def display_main_menu():
    """Display the main menu"""
    print("\n" + "="*80)
    print("WELCOME TO E-COMMERCE BACKEND SYSTEM")
    print("="*80)
    print("\n[1] PRODUCT MANAGEMENT")
    print("    [1.1] View All Products")
    print("    [1.2] Search Products")
    print("    [1.3] View Product Details")
    print("\n[2] SHOPPING CART")
    print("    [2.1] View Cart")
    print("    [2.2] Add Product to Cart")
    print("    [2.3] Update Cart Item Quantity")
    print("    [2.4] Remove Item from Cart")
    print("    [2.5] Clear Cart")
    print("\n[3] ORDERS")
    print("    [3.1] Create Order from Cart")
    print("    [3.2] View All Orders")
    print("    [3.3] View Order Details")
    print("    [3.4] Track Order")
    print("    [3.5] Update Order Status")
    print("    [3.6] Search Orders by Customer")
    print("\n[4] EXIT")
    print("="*80)
    print()

def products_menu():
    """Handle product management menu"""
    while True:
        print("\n--- PRODUCT MANAGEMENT ---")
        print("[1] View All Products")
        print("[2] Search Products")
        print("[3] View Product Details")
        print("[4] Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            list_products()
        
        elif choice == "2":
            search_term = input("Enter product name or keyword to search: ").strip()
            if search_term:
                search_product(search_term)
            else:
                print("Please enter a search term.")
        
        elif choice == "3":
            try:
                product_id = int(input("Enter product ID: ").strip())
                get_product_details(product_id)
            except ValueError:
                print("Invalid product ID. Please enter a number.")
        
        elif choice == "4":
            break
        
        else:
            print("Invalid option. Please try again.")

def cart_menu():
    """Handle shopping cart menu"""
    while True:
        print("\n--- SHOPPING CART ---")
        print("[1] View Cart")
        print("[2] Add Product to Cart")
        print("[3] Update Item Quantity")
        print("[4] Remove Item from Cart")
        print("[5] Clear Cart")
        print("[6] Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            view_cart()
        
        elif choice == "2":
            try:
                product_id = int(input("Enter product ID to add: ").strip())
                quantity = int(input("Enter quantity: ").strip())
                if quantity > 0:
                    add_to_cart(product_id, quantity)
                else:
                    print("Quantity must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        
        elif choice == "3":
            try:
                cart_id = int(input("Enter cart item ID to update: ").strip())
                new_quantity = int(input("Enter new quantity: ").strip())
                update_cart_quantity(cart_id, new_quantity)
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        
        elif choice == "4":
            try:
                cart_id = int(input("Enter cart item ID to remove: ").strip())
                remove_from_cart(cart_id)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        elif choice == "5":
            confirm = input("Are you sure you want to clear the cart? (yes/no): ").strip().lower()
            if confirm == "yes":
                clear_cart()
            else:
                print("Action cancelled.")
        
        elif choice == "6":
            break
        
        else:
            print("Invalid option. Please try again.")

def orders_menu():
    """Handle orders menu"""
    while True:
        print("\n--- ORDERS ---")
        print("[1] Create Order from Cart")
        print("[2] View All Orders")
        print("[3] View Order Details")
        print("[4] Track Order")
        print("[5] Update Order Status (Admin)")
        print("[6] Search Orders by Customer")
        print("[7] Back to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            cart_total = get_cart_total()
            if cart_total == 0:
                print("Error: Cart is empty. Cannot create order.")
            else:
                view_cart()
                customer_name = input("Enter customer name: ").strip()
                customer_email = input("Enter customer email: ").strip()
                shipping_address = input("Enter shipping address: ").strip()
                
                if customer_name and customer_email and shipping_address:
                    create_order(customer_name, customer_email, shipping_address)
                else:
                    print("Error: All fields are required.")
        
        elif choice == "2":
            list_orders()
        
        elif choice == "3":
            try:
                order_id = int(input("Enter order ID: ").strip())
                get_order_details(order_id)
            except ValueError:
                print("Invalid order ID. Please enter a number.")
        
        elif choice == "4":
            try:
                order_id = int(input("Enter order ID to track: ").strip())
                track_order(order_id)
            except ValueError:
                print("Invalid order ID. Please enter a number.")
        
        elif choice == "5":
            try:
                order_id = int(input("Enter order ID: ").strip())
                print("Valid statuses: Pending, Processing, Shipped, Delivered, Cancelled")
                new_status = input("Enter new status: ").strip()
                update_order_status(order_id, new_status)
            except ValueError:
                print("Invalid order ID. Please enter a number.")
        
        elif choice == "6":
            customer_name = input("Enter customer name to search: ").strip()
            if customer_name:
                search_orders_by_customer(customer_name)
            else:
                print("Please enter a customer name.")
        
        elif choice == "7":
            break
        
        else:
            print("Invalid option. Please try again.")

def main():
    """Main application loop"""
    print("\nInitializing E-Commerce Backend System...")
    
    # Initialize database and add sample data
    init_database()
    add_sample_products()
    
    print("✓ System initialized successfully!")
    
    while True:
        display_main_menu()
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            products_menu()
        
        elif choice == "2":
            cart_menu()
        
        elif choice == "3":
            orders_menu()
        
        elif choice == "4":
            print("\n" + "="*80)
            print("Thank you for using E-Commerce Backend System!")
            print("="*80 + "\n")
            sys.exit(0)
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)
