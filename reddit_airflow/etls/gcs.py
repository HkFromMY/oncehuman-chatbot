from google.cloud import storage
from utils.constants import (
    GCP_PROJECT_ID,
    GCP_BUCKET_NAME
)
from utils.discord import send_discord_message

def test_connection_gcs():
    """
        Check whether the connection to GCS is successful
    """
    try:
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        _ = storage_client.list_buckets()
        
    except Exception as e:
        send_discord_message(f"Error connecting to GCS: \n {repr(e)}")

        raise Exception(f"Error connecting to GCS: \n {repr(e)}")

def upload_to_gcs(src_filename, dst_filename):
    """
        Upload local file to GCS
    """
    try:
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(GCP_BUCKET_NAME)
        blob = bucket.blob(dst_filename)

        generation_match_precondition = 0
        blob.upload_from_filename(src_filename, if_generation_match=generation_match_precondition)

        print(f"File successfully uploaded to GCS. Src File: {src_filename} Dst File: {dst_filename}")

    except Exception as e:

        # send to discord
        send_discord_message(f"Error uploading local files (Src: **{src_filename}** Dst: **{dst_filename}**) to GCS: \n {repr(e)}")

        # raise exception
        raise Exception(f"Error uploading local files to GCS: \n {repr(e)}")
