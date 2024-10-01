from utils.constants import (
    REDDIT_CLIENT_ID,
    REDDIT_SECRET_KEY,
    USER_AGENT,
    SUBREDDIT,
    POST_FIELDS,
    REDDIT_HOST,
)
from utils.discord import send_discord_message
from utils.file import write_to_json, read_json

import praw 
import numpy as np
import pandas as pd 
from datetime import datetime 

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
        Upload raw JSON files to GCS
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
            post['created_utc'] = datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
            posts_list.append(post)

        # write to JSON and upload to GCS
        today = datetime.now().strftime('%Y%m%d')
        filename = f'post_{today}.json'
        write_to_json(posts_list, f'data/{filename}')

        return filename
    
    except Exception as e:
        # send to discord
        send_discord_message(f"Error extracting posts: \n {repr(e)}")

        # raise exception
        raise Exception(f"Error extracting posts: \n {repr(e)}")

def extract_comments(reddit, filename):
    """
        Extract comments from each post 
    """
    try:
        posts = read_json(f'data/{filename}')
        comments = []
        
        for post in posts:
            permalink = post['permalink']
            submission_url = REDDIT_HOST + permalink
            submission = reddit.submission(url=submission_url)

            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                cleaned_comment = {
                    'id': comment.id,
                    'post_id': post['id'],
                    'text': comment.body,
                    'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'ups': comment.ups,
                    'downs': comment.downs,
                    'likes': comment.likes
                }

                comments.append(cleaned_comment)

        today = datetime.now().strftime('%Y%m%d')
        comments_filename = f'comments_{today}.json'
        write_to_json(comments, f'data/{comments_filename}')

        return comments_filename

    except Exception as e:
        # send to discord
        send_discord_message(f"Error extracting comments (file: {filename}): \n {repr(e)}")

        # raise exception
        raise Exception(f"Error extracting comments: \n {repr(e)}")