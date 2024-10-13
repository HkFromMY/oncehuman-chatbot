from etls.postgres import (
    transform_comments_data,
)
from etls.gcs import (
    upload_to_gcs,
)
from utils.file import (
    clean_local_file,
)

def transform_comments_postgres_pipeline(ti):
    filename = transform_comments_data()

    ti.xcom_push(key='combined_doc_filename', value=filename)

def upload_combined_to_gcs_pipeline(ti):
    filename = ti.xcom_pull(key='combined_doc_filename')

    upload_to_gcs(f'data/{filename}', f'transformed/{filename}')

def clean_combined_files_pipeline(ti):
    filename = ti.xcom_pull(key='combined_doc_filename')

    clean_local_file(f'data/{filename}')
