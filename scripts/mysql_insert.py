import mysql.connector
import pandas as pd
import getpass
import json
# This will prompt you to type your password in the console securely
db_password = getpass.getpass("Enter your MySQL password: ")

print("Connecting to MySQL...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=db_password,
        database="uber_eats_db"
    )
    cursor = conn.cursor()

    print("Reading dataset...")
    df = pd.read_csv("data/processed/db_cleaned_restaurants.csv")

    cursor.execute("DROP TABLE IF EXISTS restaurants;")

    print("Creating table...")
    # Using VARCHAR(255) or similar is usually better for indexing than TEXT 
    # if you plan to search by name or location later.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_name VARCHAR(255),
        location VARCHAR(255),
        cuisines TEXT,
        rate FLOAT,
        approx_cost_for_two INT,
        online_order VARCHAR(10),
        book_table VARCHAR(10),
        price_segment VARCHAR(20),      
        rating_category VARCHAR(20)  
    )
    """)

    print("Inserting data...")
    # Optimization: Use executemany for faster insertion with large datasets
    sql = "INSERT INTO restaurants VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = [tuple(x) for x in df.values]
    cursor.executemany(sql, data)

    conn.commit()
    print(f"Successfully inserted {cursor.rowcount} rows!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")