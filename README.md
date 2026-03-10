# Uber Eats Bangalore Analytics Dashboard

- Python, Pandas, MySQL, Streamlit
- Analyzes restaurant and order data
- 15 SQL-based business questions
- Tabular decision-focused dashboard

## Folder Structure

data/           → raw and processed datasets  
scripts/        → data cleaning and MySQL insertion  
streamlit_app/  → Streamlit dashboard

## How to Run

1. Install requirements: `pip install -r requirements.txt`  
2. Clean CSV: `python scripts/data_cleaning.py`  
3. Insert restaurants: `python scripts/mysql_insert.py`  
4. Insert orders: `python scripts/json_to_sql.py`  
5. Run dashboard: `streamlit run streamlit_app/app.py`