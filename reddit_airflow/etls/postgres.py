import pandas as pd 
from sqlalchemy import create_engine
from utils.constants import (
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
)

def load_to_postgres(filename, table_name):
    """
        Accepts filename and table_name to load data from JSON files to postgres
    """
    df = pd.read_json(filename)

    # make connection to postgres
    engine = create_engine(f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

    # add data to the database
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False, chunksize=100)
    
    # close connection
    engine.dispose()
