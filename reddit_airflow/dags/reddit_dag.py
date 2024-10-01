import sys
import os 

# ensure that the path is set correctly so that the modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator 
from pipelines.reddit_pipeline import (
    extract_raw_posts_pipeline,
    upload_data_to_gcs_pipeline,
    extract_comments_pipeline,
    clean_all_localfiles_pipeline,
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
        python_callable=extract_raw_posts_pipeline,
    )

    upload_posts_gcs = PythonOperator(
        task_id='upload_raw_posts_gcs',
        python_callable=upload_data_to_gcs_pipeline,
        op_kwargs={'type': 'raw_posts'},
    )

    extract_comments = PythonOperator(
        task_id='extract_comments_pipeline',
        python_callable=extract_comments_pipeline,
    )

    upload_comments_to_gcs = PythonOperator(
        task_id='upload_comments_to_gcs',
        python_callable=upload_data_to_gcs_pipeline,
        op_kwargs={'type': 'comments'}
    )

    cleaning_localfiles = PythonOperator(
        task_id='clean_all_localfiles',
        python_callable=clean_all_localfiles_pipeline
    )

    extract_transform_post >> upload_posts_gcs >> extract_comments >> upload_comments_to_gcs >> cleaning_localfiles
    