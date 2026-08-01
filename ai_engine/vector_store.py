import os
from langchain.vectorstores import Chroma
from app.ai_engine.embedding_service import get_embeddings


def get_vector_store():
    persist_directory = os.getenv('CHROMADB_DIR', '/data/chromadb')
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=get_embeddings(),
    )
