from etls.reddit_etl import (
    connect_reddit,
    extract_posts,
    extract_comments,
    clean_post_data,
    clean_comments_data,
)
from etls.gcs import (
    test_connection_gcs,
    upload_to_gcs,
)
from etls.postgres import (
    load_to_postgres,
)
from utils.constants import DISCUSSION_TOPIC
from utils.file import clean_local_file
from utils.discord import send_discord_message

def extract_raw_posts_pipeline(ti):
    reddit = connect_reddit()

    # extract posts from Reddit with 2 tags/flairs
    output_filename = extract_posts(reddit, DISCUSSION_TOPIC)

    ti.xcom_push(key='raw_posts_filename', value=output_filename)

def upload_data_to_gcs_pipeline(type, ti):
    if type == 'raw_posts':
        upload_file = ti.xcom_pull(key='raw_posts_filename')
    elif type == 'comments':
        upload_file = ti.xcom_pull(key='comments_filename')
    else:
        send_discord_message(f"Invalid type: {type}. Please provide a valid type: ['raw_posts', 'comments'] at upload_data_to_gcs_pipeline()")
        raise Exception(f"Invalid type: {type}. Please provide a valid type: ['raw_posts', 'comments']")

    print(f'Uploading file: {upload_file}')

    src_filename = f'data/{upload_file}'
    dst_filename = f'{type}/{upload_file}'

    # test if the connection to GCS is successful, raise Exception if not success
    test_connection_gcs()

    # upload local files to GCS
    upload_to_gcs(src_filename, dst_filename)

def extract_comments_pipeline(ti):
    reddit = connect_reddit() 

    post_filename = ti.xcom_pull(key='raw_posts_filename')

    comments_filename = extract_comments(reddit, post_filename)

    ti.xcom_push(key='comments_filename', value=comments_filename)

def transform_data_pipeline(ti):
    post_filename = ti.xcom_pull(key='raw_posts_filename')
    comments_filename = ti.xcom_pull(key='comments_filename')

    clean_post_data(f'data/{post_filename}')
    clean_comments_data(f'data/{comments_filename}')

def load_to_postgres_pipeline(ti):
    post_filename = ti.xcom_pull(key='raw_posts_filename')
    comments_filename = ti.xcom_pull(key='comments_filename')

    load_to_postgres(f'data/{post_filename}', 'reddit_posts')
    load_to_postgres(f'data/{comments_filename}', 'reddit_comments')

def clean_all_localfiles_pipeline(ti):
    post_filename = ti.xcom_pull(key='raw_posts_filename')
    comments_filename = ti.xcom_pull(key='comments_filename')

    clean_local_file(f'data/{post_filename}')
    clean_local_file(f'data/{comments_filename}')
