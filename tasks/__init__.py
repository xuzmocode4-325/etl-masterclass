from airflow.sdk import dag, task
from datetime import datetime, timedelta

from tasks.check_updates import check_updates
from tasks.load_updates import load_data_to_snowflake
from tasks.update_facts import update_fact_table

default_args = {
    'owner': 'your_name',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='etl_snowflake',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    catchup=False,
    **default_args
) 
def update_data_taskflow():
    
    date = None
    products = None
    
    @task()
    def check():
        check_updates(date, products)
    
    @task()
    def load():
        load_data_to_snowflake()


    @task()
    def update():
        update_fact_table()


    if check(): 
        load()
        update()
        
update_data_taskflow()