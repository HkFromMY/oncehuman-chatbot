from utils.constants import (
    REDDIT_CLIENT_ID,
    REDDIT_SECRET_KEY,
    USER_AGENT,
    SUBREDDIT,
    POST_FIELDS,
)
from utils.discord import send_discord_message

import praw 
import numpy as np
import pandas as pd 
from datetime import datetime 
import json 

def connect_reddit():
    """
        Create Reddit instance using praw library and connect to reddit
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET_KEY,
            user_agent=USER_AGENT,
        )

        return reddit
    
    except Exception as e:
        # send to discord
        send_discord_message(f"Error connecting to Reddit: \n {repr(e)}")

        # raise exception
        raise Exception(f"Error connecting to Reddit: \n {repr(e)}")
    
def extract_posts(reddit, query):
    """
        Extract posts from reddit
        Load extracted posts to JSON file for future processing
    """
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        posts = subreddit.search(
            query=query,
            sort='top',
            time_filter='day',
            limit=50,  
        )

        posts_list = []
        for post in posts:
            post_dict = vars(post)
            post = { field: post_dict[field] for field in POST_FIELDS }
            posts_list.append(post)

        # write to JSON and upload to GCS
        topic = query.split(':')[-1]
        today = datetime.now().strftime('%Y%m%d')
        filename = f'post_{today}.json'
        with open(f'data/{filename}', 'w') as f:
            json.dump(posts_list, f)

        return filename
    
    except Exception as e:
        # send to discord
        send_discord_message(f"Error extracting posts: \n {repr(e)}")

        # raise exception
        raise Exception(f"Error extracting posts: \n {repr(e)}")

def transform_data():
    """
        Extract comments from each post and transform the data 
    """
    pass 
