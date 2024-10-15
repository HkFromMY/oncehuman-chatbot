from datetime import datetime, timedelta 
from airflow import DAG
from airflow.decorators import task 
from airflow.operators.bash import BashOperator 
from airflow.operators.python import PythonOperator

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd 
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface.embeddings.huggingface_endpoint import HuggingFaceEndpointEmbeddings
from utils.constants import EMBEDDING_MODEL_NAME, HUGGINGFACEHUB_API_TOKEN
# First DAG to see if the environment is working

default_args = {
    'owner': 'me',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

from google.cloud import storage
from etls.gcs import test_connection_gcs, upload_to_gcs

def connect_gcs():
    try:
        storage_client = storage.Client(project='reddit-data-engineering')
        buckets = storage_client.list_buckets()
        print("Buckets:")
        for bucket in buckets:
            print(bucket.name)
        print("Listed all storage buckets.")

    except Exception as e:
        print("Failed connecting to GCS:\n\n")
        print(e)
        raise Exception(e)

with DAG(
    dag_id='first_dag',
    description='first_dag',
    default_args=default_args,
    start_date=datetime(2024, 9, 1),
    schedule='@daily',
    catchup=False,
) as dag:
    hello_world = BashOperator(
        task_id='hello_world',
        bash_command='echo "Hello World!"'
    )

    embed = PythonOperator(
        task_id='embed',
        python_callable=embed_something
    )

    hello_world >> embed