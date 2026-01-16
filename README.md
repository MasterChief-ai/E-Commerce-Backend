# E-Commerce Backend System

A command-line based e-commerce application built with Python and SQLite, featuring product listing, shopping cart management, and order tracking functionality.

## Features

### 1. Product Management
- **View All Products**: Display all available products with pricing and stock information
- **Search Products**: Search products by name or description
- **Product Details**: View detailed information about specific products

### 2. Shopping Cart
- **Add to Cart**: Add products with quantity selection
- **View Cart**: Display all items in cart with total cost calculation
- **Update Quantity**: Modify quantities of items in cart
- **Remove Items**: Delete specific items from cart
- **Clear Cart**: Empty entire cart at once
- **Stock Management**: Automatic stock validation before adding items

### 3. Order Management
- **Create Orders**: Convert cart items into orders with customer information
- **Order Tracking**: Track order status with timeline visualization
- **Order History**: View all orders sorted by date
- **Order Details**: View detailed breakdown of items in specific orders
- **Update Status**: Admin function to update order status (Pending → Processing → Shipped → Delivered)
- **Search Orders**: Find orders by customer name

## Project Structure

```
E-Commerce Backend/
├── main.py                 # Main application entry point with CLI menu
├── database.py            # Database initialization and connection management
├── products.py            # Product listing and search functionality
├── cart.py               # Shopping cart operations
├── orders.py             # Order management and tracking
├── requirements.txt      # Python package dependencies
└── ecommerce.db         # SQLite database (auto-generated on first run)
```

## Database Schema

### Products Table
- `product_id` - Primary key
- `name` - Product name
- `description` - Product description
- `price` - Product price
- `stock` - Available quantity
- `created_at` - Timestamp

### Cart Table
- `cart_item_id` - Primary key
- `product_id` - Foreign key (products)
- `quantity` - Item quantity
- `added_at` - Timestamp

### Orders Table
- `order_id` - Primary key
- `customer_name` - Customer name
- `customer_email` - Customer email
- `shipping_address` - Delivery address
- `total_amount` - Order total
- `status` - Order status (Pending, Processing, Shipped, Delivered, Cancelled)
- `order_date` - Timestamp

### Order Items Table
- `order_item_id` - Primary key
- `order_id` - Foreign key (orders)
- `product_id` - Foreign key (products)
- `quantity` - Item quantity
- `unit_price` - Price at time of order

## Installation

1. **Clone/Extract the project**
   ```bash
   cd "E-Commerce Backend"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install tabulate
   ```
   (sqlite3 is included with Python by default)

## Usage

Run the application:
```bash
python main.py
```

The application will:
1. Initialize the SQLite database automatically
2. Load 10 sample products
3. Display the main menu

### Example Workflow

1. **Browse Products**
   - Select option 1.1 to view all products
   - Use option 1.2 to search for specific items
   - Choose 1.3 to see detailed information

2. **Add to Cart**
   - Select option 2.2
   - Enter product ID and quantity
   - View cart with option 2.1

3. **Create Order**
   - Review cart (option 2.1)
   - Select option 3.1 to create order
   - Enter customer details
   - Order confirmation will be displayed

4. **Track Orders**
   - Use option 3.4 to track order status
   - Option 3.3 shows order details
   - Option 3.6 searches orders by customer

## Sample Products

The system comes preloaded with 10 sample products:
- Wireless Mouse
- USB-C Cable
- Mechanical Keyboard
- Monitor Stand
- Laptop Cooling Pad
- Webcam HD
- USB Hub
- Screen Protector
- Desk Lamp
- Cable Organizer

## Key Features Implementation

### Stock Management
- Real-time stock validation
- Automatic stock deduction upon order creation
- Prevents overselling

### Data Persistence
- SQLite database for reliable data storage
- Foreign key relationships for data integrity
- Automatic timestamp tracking

### User-Friendly Interface
- Menu-driven CLI navigation
- Formatted table displays using tabulate
- Clear error messages and confirmations
- Status tracking with visual timeline

## Technical Stack

- **Language**: Python 3.13+
- **Database**: SQLite3
- **Dependencies**: 
  - tabulate (for formatted output)
- **Architecture**: Modular design with separate modules for each feature


## Group Members

Add your group member names here:
- [Name] - [Matric No]
- [Name] - [Matric No]
- [Name] - [Matric No]
- [Name] - [Matric No]

## Future Enhancements

Possible improvements:
- User authentication and login
- Multiple user accounts with saved carts
- Payment gateway integration
- Email notifications
- Advanced product filtering (by price range, category)
- Inventory reports and analytics
- Return/refund management

## Notes

- The database is automatically created on first run
- Sample products are only added if the database is empty
- All monetary values are stored as floats for precision
- Order status follows a workflow: Pending → Processing → Shipped → Delivered

## Troubleshooting

**Issue: `ModuleNotFoundError: No module named 'tabulate'`**
- Solution: Run `pip install tabulate`

**Issue: Database locked error**
- Solution: Ensure only one instance of the application is running

**Issue: Sample products not loading**
- Solution: Delete `ecommerce.db` and restart the application

## License

This is a school project. Feel free to modify and enhance as needed.
