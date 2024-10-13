import json 
from .discord import send_discord_message
import os 

def write_to_json(data, filename):
    """
        Write data to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)

    except Exception as e:
        send_discord_message(f'Error writing to JSON (file: {filename}): \n {repr(e)}')

        raise Exception(f"Error writing to JSON: \n {repr(e)}")
    
def read_json(filename):
    """
        Read data from JSON file
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        return data 
    
    except Exception as e:
        send_discord_message(f'Error reading from JSON (file: {filename}): \n {repr(e)}')

        raise Exception(f"Error reading from JSON: \n {repr(e)}")
    
def clean_local_file(filename):
    """
        Delete all local files on airflow after uploading to GCS
    """
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File: {filename} removed successfully")

    else:
        send_discord_message(f'WARNING: File does not exist [FILE: {filename}]. No file removed.')
    