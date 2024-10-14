from datetime import datetime 
import pandas as pd 
from sqlalchemy import create_engine 
from utils.constants import (
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
)
from utils.discord import send_discord_message

def transform_comments_data():
    """
        Concatenate all comments of the same post and joined with post data to create new document
        Then load the new document into a new table and file (for GCS). 
    """
    try:
        today = datetime.now().strftime('%Y%m%d')
        today_sql = datetime.now().strftime('%Y-%m-%d') # used in query for filtering
        combined_filename = f'reddit_docs_{today}.json'

        engine = create_engine(f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        comments_df = pd.read_sql_query(f"SELECT * FROM \"reddit_comments\" WHERE DATE_TRUNC('day', created_at) = '{today_sql}';", con=engine)
        posts_df = pd.read_sql_query(f"SELECT * FROM \"reddit_posts\" WHERE DATE_TRUNC('day', created_at) = '{today_sql}';", con=engine)
        
        comments_df['concatenated_comments_text'] = comments_df.groupby('post_id')['text'].transform(lambda x: '\n\n'.join(x))
        comments_df = comments_df[['post_id', 'concatenated_comments_text']].drop_duplicates()
        
        # join both comments and posts table
        combined_df = pd.merge(posts_df, comments_df, left_on='id', right_on='post_id', how='left')
        combined_df['document'] = '### Post Content\n' + combined_df['title'] + '\n\n' + combined_df['selftext'] + '\n\n###Discussion/Answer:\n' + combined_df['concatenated_comments_text']
        combined_df = combined_df.rename(columns={'id': 'doc_id'})[['doc_id', 'document']]
        combined_df = combined_df.dropna(subset=['document']) # remove NULL

        # load to postgres new table and to file (to upload to GCS)
        combined_df.to_sql(name="reddit_docs", con=engine, if_exists='append', index=False, chunksize=100) 
        combined_df.to_json(f'data/{combined_filename}', mode='w', orient='records', indent=4)

        return combined_filename
    
    except Exception as e:
        send_discord_message(f"Error transforming comments data: \n {repr(e)}")
        raise Exception(f"Error transforming comments data: \n {repr(e)}")

    finally:
        engine.dispose()