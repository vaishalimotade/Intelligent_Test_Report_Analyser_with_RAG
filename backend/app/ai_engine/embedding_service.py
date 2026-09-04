import os

from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    return OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL"),
        check_embedding_ctx_length=False,
    )
