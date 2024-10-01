import sys
import os 

# ensure that the path is set correctly so that the modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator 
from pipelines.reddit_pipeline import (
    extract_raw_posts,
    upload_raw_posts_gcs
)

default_args = {
    'owner': 'me',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='reddit_dag_pipeline',
    description='A data pipeline that ingest and transform data from Reddit and load to postgres',
    default_args=default_args,
    start_date=datetime(2024, 9, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    extract_transform_post = PythonOperator(
        task_id='extract_raw_posts',
        python_callable=extract_raw_posts,
    )

    upload_raw_gcs = PythonOperator(
        task_id='upload_raw_posts_gcs',
        python_callable=upload_raw_posts_gcs,
    )

    extract_transform_post >> upload_raw_gcs
    