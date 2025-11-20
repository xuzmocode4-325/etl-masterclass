import os
import sqlite3
import pandas as pd

data_path = os.getenv('DATA_PATH')
db_conn = os.getenv('AIRFLOW__DATABASE__SQL_ALCHEMY_CONN')

def get_last_processed_date():
    if db_conn:
        try:
            with sqlite3.connect(db_conn) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT MAX(sales_date) FROM sales_data
                """)
                result = cur.fetchone()
                if result:
                    return result[0]  # max sales_date
                return None
        except Exception as e:
            print(f"Error getting last processed date: {e}")
    return None
    


def get_product_ids():
    if db_conn:
        try:
            with sqlite3.connect(db_conn) as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT DISTINCT product_id FROM sales_data
                """)
                products = cur.fetchall()
                return [row[0] for row in products]  # list of product_ids
        except Exception as e:
            print(f"Error getting product IDs: {e}")
    return []


def detect_sales_update(last_processed_date):
    sales = pd.read_csv(f'{data_path}/daily_sales.csv', parse_dates=['date'])
    max_date = sales['date'].max()
    return max_date > last_processed_date


def detect_new_products(processed_product_ids):
    products = pd.read_json(f'{data_path}/product_info.json')
    new_ids = set(products['product_id']) - set(processed_product_ids)
    return len(new_ids) > 0


def check_updates():
        last_processed_date = get_last_processed_date()
        processed_product_ids = get_product_ids()

        sales_updated = detect_sales_update(last_processed_date)
        products_updated = detect_new_products(processed_product_ids)
        return sales_updated or products_updated