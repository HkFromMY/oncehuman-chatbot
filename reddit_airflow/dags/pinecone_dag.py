import sys
import os 

# ensure that the path is set correctly so that the modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator 
from airflow.utils.trigger_rule import TriggerRule
from pipelines.pinecone_pipeline import (
    load_documents_to_pinecone_pipeline,
)

default_args = {
    'owner': 'me',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pinecone_dag',
    description='A pipeline that embeds the textual data from transformed comments, then load the embedding vectors to PostgreSQL',
    default_args=default_args,
    start_date=datetime(2024, 9, 1),
    schedule_interval='0 2 * * *', # 1 hour after the transform pipeline
    catchup=False,
) as dag:
    
    load_documents_to_pinecone = PythonOperator(
        task_id='load_documents_to_pinecone',
        python_callable=load_documents_to_pinecone_pipeline,
    )

    load_documents_to_pinecone
