import os
from langchain.embeddings.openai import OpenAIEmbeddings


def get_embeddings():
    return OpenAIEmbeddings(
        deployment=os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'text-embedding-3-large'),
    )
