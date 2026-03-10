import streamlit as st
import mysql.connector
from qa_page import show_qa_page  # import the function
import pandas as pd

st.title("Uber Eats Bangalore Analytics Dashboard")

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Monisha@1207",
    database="uber_eats_db"
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Q&A Page", "Order Analytics"]
)

# Show pages
if page == "Dashboard":
    st.header("Restaurant Dataset")
    df = pd.read_sql("SELECT * FROM restaurants LIMIT 100", conn)
    st.dataframe(df)

elif page == "Q&A Page":
    show_qa_page(conn)  # call the function from qa_page.py

elif page == "Order Analytics":
    st.header("Order Insights")
    df = pd.read_sql("""
        SELECT payment_method, COUNT(*) AS total_orders
        FROM orders
        GROUP BY payment_method
    """, conn)
    st.dataframe(df)