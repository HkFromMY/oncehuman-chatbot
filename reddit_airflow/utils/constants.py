import configparser 
import os 

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

# DISCORD WEBHOOK
DISCORD_WEBHOOK = parser.get('discord', 'discord_webhook')

# reddit credentials 
REDDIT_CLIENT_ID = parser.get('reddit', 'reddit_client_id')
REDDIT_SECRET_KEY = parser.get('reddit', 'reddit_secret_key')
USER_AGENT = parser.get('reddit', 'reddit_user_agent')
SUBREDDIT = parser.get('reddit', 'subreddit')
BUILD_TOPIC = parser.get('reddit', 'build_topic')
DISCUSSION_TOPIC = parser.get('reddit', 'discussion_topic')
REDDIT_HOST = parser.get('reddit', 'host')

# database credentials 
DATABASE_HOST = parser.get('database', 'database_host')
DATABASE_NAME = parser.get('database', 'database_name')
DATABASE_PORT = parser.get('database', 'database_port')
DATABASE_USERNAME = parser.get('database', 'database_username')
DATABASE_PASSWORD = parser.get('database', 'database_password')
DATABASE_POSTS_TABLE = parser.get('database', 'post_table')
DATABASE_COMMENTS_TABLE = parser.get('database', 'comment_table')

# GCP 
GCP_PROJECT_ID = parser.get('gcp', 'project_id')
GCP_BUCKET_NAME = parser.get('gcp', 'bucket_name')

# pinecone 
PINECONE_API_KEY = parser.get('pinecone', 'pinecone_api_key')
PINECONE_INDEX_NAME = parser.get('pinecone', 'pinecone_index_name')
PINECONE_INDEX_DIMENSION = int(parser.get('pinecone', 'pinecone_index_dimension'))

# langchain config
CHUNK_SIZE = int(parser.get('langchain', 'chunk_size'))
CHUNK_OVERLAP = int(parser.get('langchain', 'chunk_overlap'))
EMBEDDING_MODEL_NAME = parser.get('langchain', 'embedding_model_name')
HUGGINGFACEHUB_API_TOKEN = parser.get('langchain', 'huggingfacehub_api_token')

POST_FIELDS = [
    'id',
    'selftext',
    'title',
    'created_utc',
    'upvote_ratio',
    'num_comments',
    'permalink',
]
