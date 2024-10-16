import pandas as pd 
from psycopg2 import IntegrityError
from sqlalchemy import create_engine
from utils.constants import (
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
)
from utils.discord import send_discord_message

def load_to_postgres(filename, table_name):
    """
        Accepts filename and table_name to load data from JSON files to postgres
    """
    try:
        df = pd.read_json(filename)

        # make connection to postgres
        engine = create_engine(f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

        # add data to the database
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False, chunksize=100)

    except IntegrityError as e:
        # just skip this schedule, the next day should be fine when everything is on schedule
        send_discord_message(f"Duplicated keys found when loading data to {table_name}: \n {repr(e)}")
        
    except Exception as e:
        send_discord_message(f"Error loading posts/comments data to postgres: \n {repr(e)}")

        raise Exception(f"Error loading posts/comments data to postgres: \n {repr(e)}")
    
    finally:
        # close connection
        engine.dispose()
