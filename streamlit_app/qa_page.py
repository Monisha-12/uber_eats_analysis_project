# qa_page.py
import streamlit as st
import pandas as pd

def show_qa_page(conn):
    st.header("Business Questions & Insights")

    # 1️⃣ Top 10 locations by average rating
    st.subheader("1. Top 10 Locations by Average Restaurant Ratings")
    query = """
    SELECT location, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY location
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 2️⃣ Over-saturated locations
    st.subheader("2. Locations with Most Restaurants (Over-Saturated)")
    query = """
    SELECT location, COUNT(*) AS num_restaurants
    FROM restaurants
    GROUP BY location
    ORDER BY num_restaurants DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 3️⃣ Online ordering impact on ratings
    st.subheader("3. Average Rating: Online Ordering vs No Online Ordering")
    query = """
    SELECT online_order, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY online_order;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 4️⃣ Table booking impact on ratings
    st.subheader("4. Average Rating: Table Booking vs No Table Booking")
    query = """
    SELECT book_table, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY book_table;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 5️⃣ Best price range
    st.subheader("5. Average Rating by Price Segment")
    query = """
    SELECT price_segment, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY price_segment
    ORDER BY avg_rating DESC;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 6️⃣ Most common cuisines
    st.subheader("6. Top 10 Most Common Cuisines")
    query = """
    SELECT cuisines, COUNT(*) AS num_restaurants
    FROM restaurants
    GROUP BY cuisines
    ORDER BY num_restaurants DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 7️⃣ Highest rated cuisines
    st.subheader("7. Top 10 Highest Rated Cuisines")
    query = """
    SELECT cuisines, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY cuisines
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 8️⃣ Niche high-quality cuisines
    st.subheader("8. Niche Cuisines with Few Restaurants but High Ratings")
    query = """
    SELECT cuisines, COUNT(*) AS num_restaurants, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY cuisines
    HAVING num_restaurants < 10
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 9️⃣ Relation: Cost vs Rating
    st.subheader("9. Average Rating by Price Range")
    query = """
    SELECT approx_cost_for_two AS price_range, ROUND(AVG(rate),2) AS avg_rating
    FROM restaurants
    GROUP BY approx_cost_for_two
    ORDER BY price_range;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 🔟 Top 10 restaurants by number of orders
    st.subheader("10. Top 10 Restaurants by Number of Orders")
    query = """
    SELECT restaurant_name, COUNT(*) AS total_orders
    FROM orders
    GROUP BY restaurant_name
    ORDER BY total_orders DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 11️⃣ Orders by payment method
    st.subheader("11. Orders by Payment Method")
    query = """
    SELECT payment_method, COUNT(*) AS total_orders
    FROM orders
    GROUP BY payment_method;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 12️⃣ Orders using discounts
    st.subheader("12. Orders Using Discounts")
    query = """
    SELECT discount_used, COUNT(*) AS total_orders
    FROM orders
    GROUP BY discount_used;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 13️⃣ Average order value per restaurant
    st.subheader("13. Average Order Value per Restaurant")
    query = """
    SELECT restaurant_name, ROUND(AVG(order_value),2) AS avg_order_value
    FROM orders
    GROUP BY restaurant_name
    ORDER BY avg_order_value DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 14️⃣ Highest revenue restaurants
    st.subheader("14. Highest Revenue Restaurants")
    query = """
    SELECT restaurant_name, ROUND(SUM(order_value),2) AS revenue
    FROM orders
    GROUP BY restaurant_name
    ORDER BY revenue DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

    # 15️⃣ Locations ideal for premium restaurants
    st.subheader("15. Locations Ideal for Premium Restaurants")
    query = """
    SELECT location, ROUND(AVG(rate),2) AS avg_rating, ROUND(AVG(approx_cost_for_two),0) AS avg_cost
    FROM restaurants
    GROUP BY location
    ORDER BY avg_rating DESC, avg_cost DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)