import sqlite3

def update_fact_table():
    # Connect to the local SQLite database file
    conn = sqlite3.connect('/absolute/path/to/your/local_airflow.db')

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Example: Drop/recreate the fact table (could also run incremental SQL)
    cur.execute("""
        CREATE OR REPLACE TABLE sales_fact AS
        SELECT sd.store_id, pi.product_name, pi.product_price, sd.units_sold, sd.sales_amount
        FROM sales_data sd
        LEFT JOIN product_info pi ON sd.product_id = pi.product_id
    """)
    conn.close()
