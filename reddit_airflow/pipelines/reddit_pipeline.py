from etls.reddit_etl import (
    connect_reddit,
    extract_posts,
)
from etls.gcs import (
    test_connection_gcs,
    upload_to_gcs,
    clean_local_file,
)
from utils.constants import DISCUSSION_TOPIC

def extract_raw_posts(ti):
    reddit = connect_reddit()

    # extract posts from Reddit with 2 tags/flairs
    output_filename = extract_posts(reddit, DISCUSSION_TOPIC)

    ti.xcom_push(key='raw_posts_filename', value=output_filename)

def upload_raw_posts_gcs(ti):
    upload_file = ti.xcom_pull(key='raw_posts_filename')

    print(f'Uploading file: {upload_file}')

    src_filename = f'data/{upload_file}'
    dst_filename = f'raw_posts/{upload_file}'

    # test if the connection to GCS is successful
    test_connection_gcs()

    # upload local files to GCS
    upload_to_gcs(src_filename, dst_filename)

    # clean up local files
    clean_local_file(src_filename)
