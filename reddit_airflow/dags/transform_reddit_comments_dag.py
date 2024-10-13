import sys
import os 

# ensure that the path is set correctly so that the modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator 
from airflow.utils.trigger_rule import TriggerRule
from pipelines.transform_reddit_comments_pipeline import (
    transform_comments_postgres_pipeline,
    upload_combined_to_gcs_pipeline,
    clean_combined_files_pipeline,
)

default_args = {
    'owner': 'me',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='transform_reddit_comments',
    description='A pipeline that transforms (post-process) Reddit comments data to form new document',
    default_args=default_args,
    start_date=datetime(2024, 9, 1),
    schedule_interval='0 1 * * *', # 1 hour after the extract and load pipeline
    catchup=False,
) as dag:
    
    # transform comment data and load to postgres/GCS
    transform_comments = PythonOperator(
        task_id='transform_comments',
        python_callable=transform_comments_postgres_pipeline,
    )

    # upload the JSON file to GCS
    upload_combined_to_gcs = PythonOperator(
        task_id='upload_combined_to_gcs',
        python_callable=upload_combined_to_gcs_pipeline,
    )

    # clean the local file
    clean_combined_files = PythonOperator(
        task_id='clean_combined_files',
        python_callable=clean_combined_files_pipeline,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    transform_comments >> upload_combined_to_gcs >> clean_combined_files

    