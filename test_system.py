#!/usr/bin/env python3
"""
Test script to verify E-Commerce Backend functionality
"""

import os
import sys

# Add the project directory to path
sys.path.insert(0, r'c:\Users\MasterChief\Desktop\E-Commerce Backend')

from database import init_database, add_sample_products, get_connection
from products import list_products
from cart import add_to_cart, view_cart, get_cart_total
from orders import create_order, list_orders

def test_system():
    """Run basic functionality tests"""
    print("="*80)
    print("TESTING E-COMMERCE BACKEND SYSTEM")
    print("="*80)
    
    # Test 1: Initialize database
    print("\n[TEST 1] Initializing database...")
    try:
        init_database()
        add_sample_products()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 2: List products
    print("\n[TEST 2] Listing products...")
    try:
        list_products()
        print("✓ Products listed successfully")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 3: Add to cart
    print("\n[TEST 3] Adding product to cart...")
    try:
        add_to_cart(1, 2)  # Add product 1, quantity 2
        print("✓ Product added to cart")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 4: View cart
    print("\n[TEST 4] Viewing cart...")
    try:
        items = view_cart()
        print(f"✓ Cart viewed successfully ({len(items)} items)")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 5: Get cart total
    print("\n[TEST 5] Getting cart total...")
    try:
        total = get_cart_total()
        print(f"✓ Cart total calculated: ${total:.2f}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 6: Create order
    print("\n[TEST 6] Creating order from cart...")
    try:
        success = create_order("John Doe", "john@example.com", "123 Main St, City, State")
        if success:
            print("✓ Order created successfully")
        else:
            print("✗ Order creation failed")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    # Test 7: List orders
    print("\n[TEST 7] Listing orders...")
    try:
        list_orders()
        print("✓ Orders listed successfully")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED!")
    print("="*80)
    print("\nThe E-Commerce Backend system is ready to use.")
    print("Run 'python main.py' to start the application.")
    print()
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
