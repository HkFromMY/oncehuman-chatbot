from etls.pinecone_etl import (
    create_pinecone_index,
    load_documents_from_postgres,
    split_documents_to_chunks,
    load_documents_to_pinecone,
)

def load_documents_to_pinecone_pipeline():
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
    load_documents_to_pinecone(index, chunked_docs)
