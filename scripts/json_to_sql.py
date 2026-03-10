import mysql.connector
from mysql.connector import Error
import pandas as pd
import getpass
import json

db_password = getpass.getpass("Enter your MySQL password: ")

try:
    # First, let's see what's in the JSON
    df = pd.read_json("data/raw/orders.json")
    print("JSON columns:", df.columns.tolist())
    print("\nFirst row:")
    print(df.iloc[0])
    
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="uber_eats_db"
    )
    cursor = conn.cursor()
    
    # Drop existing table
    cursor.execute("DROP TABLE IF EXISTS orders")
    
    # Create table with flexible schema (using TEXT for everything initially)
    cursor.execute("""
    CREATE TABLE orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id VARCHAR(100),
        restaurant_name VARCHAR(255),
        order_date VARCHAR(50),
        order_value VARCHAR(50),
        discount_used VARCHAR(50),
        payment_method VARCHAR(50),
        original_data JSON
    )
    """)
    
    # Insert data with original JSON as backup
    insert_sql = """
    INSERT INTO orders (order_id, restaurant_name, order_date, order_value, discount_used, payment_method, original_data)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    data = []
    for _, row in df.iterrows():
        # Try to map columns intelligently
        order_id = row.get('order_id', row.get('Order ID', row.get('id', '')))
        restaurant = row.get('restaurant_name', row.get('Restaurant', row.get('restaurant', '')))
        order_date = row.get('order_date', row.get('Date', row.get('date', '')))
        
        # Try different possible column names for amount
        order_value = row.get('order_value', row.get('order_amount', row.get('amount', row.get('total', ''))))
        
        discount = row.get('discount_used', row.get('discount', row.get('Discount', 'No')))
        payment = row.get('payment_method', row.get('payment', row.get('Payment', '')))
        
        # Convert row to JSON for backup
        original_json = json.dumps(row.to_dict())
        
        data.append((str(order_id), str(restaurant), str(order_date), str(order_value), 
                    str(discount), str(payment), original_json))
    
    cursor.executemany(insert_sql, data)
    conn.commit()
    
    print(f"Inserted {len(data)} rows!")
    
    # Show what was inserted
    cursor.execute("SELECT id, order_id, restaurant_name, order_value FROM orders LIMIT 5")
    for row in cursor.fetchall():
        print(row)
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()