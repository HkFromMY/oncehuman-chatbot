from datetime import datetime, timedelta 
from airflow import DAG
from airflow.decorators import task 
from airflow.operators.bash import BashOperator 

import praw

# First DAG to see if the environment is working

default_args = {
    'owner': 'me',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

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

    hello_world