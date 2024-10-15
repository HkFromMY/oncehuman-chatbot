from etls.pinecone_etl import (
    create_pinecone_index,
    load_documents_from_postgres,
    split_documents_to_chunks,
    load_documents_to_pinecone,
    retry_upload_to_pinecone,
)
from utils.file import clean_local_file

def load_documents_to_pinecone_pipeline(ti):
    """
        A pipeline that embeds the textual data from transformed comments, then load the embedding vectors to PostgreSQL
    """
    # create pinecone index
    index = create_pinecone_index()

    # load documents from postgres
    documents = load_documents_from_postgres()

    # split documents into chunks
    chunked_docs = split_documents_to_chunks(documents)

    # load documents to pinecone
    failed_doc_filename = load_documents_to_pinecone(index, chunked_docs)
    ti.xcom_push(key='failed_doc_filename', value=failed_doc_filename)

def load_failed_docs_to_pinecone_pipeline(ti):
    """
        A pipeline that retry to upload the failed documents from upstream task
    """
    failed_doc_filename = ti.xcom_pull(key='failed_doc_filename')
    
    if failed_doc_filename != '':
        retry_upload_to_pinecone(f'data/{failed_doc_filename=}')

def clean_all_localfiles_pipeline(ti):
    """
        A pipeline that clean all local files after loading the failed documents to Pinecone
    """
    failed_doc_filename = ti.xcom_pull(key='failed_doc_filename')

    if failed_doc_filename != '':
        clean_local_file(f'data/{failed_doc_filename}')


