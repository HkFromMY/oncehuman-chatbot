from utils.discord import send_discord_message
from utils.constants import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_INDEX_DIMENSION,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL_NAME,
    REDDIT_HOST,
    HUGGINGFACEHUB_API_TOKEN,
)
from pinecone import Pinecone, ServerlessSpec
import time

from langchain_huggingface.embeddings.huggingface_endpoint import HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
from uuid import uuid4

def create_pinecone_index():
    """
        Create a Pinecone Index using th API Key for interaction
    """
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        existing_indexes = [index_info['name'] for index_info in pc.list_indexes()]

        if PINECONE_INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=PINECONE_INDEX_DIMENSION, # refers to the embedding models used
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1'),
            )
            while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
                time.sleep(1)

        index = pc.Index(PINECONE_INDEX_NAME)

        return index
        
    except Exception as e:
        send_discord_message(f"Error creating Pinecone Index: \n {repr(e)}")

        raise Exception(f"Something wrong when creating Pinecone Index: \n {repr(e)}")

def load_documents_from_postgres():
    """
        Load documents data from Postgres (only for the date that this function is executed)
        Return Document object to the function caller for further processing
    """
    try:
        today_sql = datetime.now().strftime('%Y-%m-%d')
        engine = create_engine(f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        doc_df = pd.read_sql_query(f'SELECT * FROM \"reddit_docs\" WHERE DATE_TRUNC(\'day\', created_at) = \'{today_sql}\';', con=engine)
        post_df = pd.read_sql_query(f'SELECT * FROM \"reddit_posts\" WHERE DATE_TRUNC(\'day\', created_at) = \'{today_sql}\';', con=engine)
        joined_df = pd.merge(doc_df, post_df, how='left', left_on='doc_id', right_on='id')

        joined_df['created_at_str'] = joined_df['created_at_x'].dt.strftime('%Y-%m-%d %H:%M:%S')
        joined_df['source_url'] = REDDIT_HOST + joined_df['permalink']

        documents = []
        for _, row in joined_df.iterrows():
            documents.append(
                Document(
                    page_content=row['document'],
                    metadata={ 'created_at': row['created_at_str'], 'source': 'reddit', 'source_url': row['source_url'], 'id': row['doc_id'] },
                )
            )

        return documents
    
    except Exception as e:
        send_discord_message(f"Error loading documents from Postgres: \n {repr(e)}")

        raise Exception(f"Something wrong when loading documents from Postgres: \n {repr(e)}")

def split_documents_to_chunks(documents):
    """
        Split documents into chunks for better performance and retrieval
    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        docs = splitter.split_documents(documents=documents)

        return docs
    
    except Exception as e:
        send_discord_message(f"Error encountered when chunking the documents: \n {repr(e)}")

        raise Exception(f"Error encountered when chunking the documents: \n {repr(e)}")

def load_documents_to_pinecone(pc_index, chunked_docs):
    """
        Load split data to Pinecone
    """
    try:
        embedding_model = HuggingFaceEndpointEmbeddings(model=EMBEDDING_MODEL_NAME, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)
        vector_store = PineconeVectorStore(index=pc_index, embedding=embedding_model)

        ids = [str(uuid4()) for _ in range(len(chunked_docs))]
        vector_store.add_documents(documents=chunked_docs, ids=ids)

    except Exception as e:
        send_discord_message(f"Error loading chunked documents to Pinecone: \n {repr(e)}")

        raise Exception(f"Something wrong when loading chunked documents to Pinecone: \n {repr(e)}")
