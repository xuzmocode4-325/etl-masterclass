import os
import sqlite3
import pandas as pd

db_conn = os.getenv('AIRFLOW__DATABASE__SQL_ALCHEMY_CONN')
def load_data_to_db():
    if db_conn:
        try:
            with sqlite3.connect(db_conn) as conn:
                sales = pd.read_csv('data/daily_sales.csv', parse_dates=['date'])
                products = pd.read_json('data/product_info.json')
                
                products.to_sql("PRODUCT_INFO", conn, if_exists='replace', index=False)
                sales.to_sql("SALES_DATA", conn, if_exists='replace', index=False)
                
                print("Data loaded successfully")
        except Exception as e:
            print("Error loading data:", e)
