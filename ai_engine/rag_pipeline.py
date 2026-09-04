import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.ai_engine.embedding_service import get_embeddings
from app.ai_engine.vector_store import get_vector_store

MODEL_NAME = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini')


def retrieve_similar_failures(test_name: str):
    vector_store = get_vector_store()
    query = f"Find similar failures for {test_name}"
    results = vector_store.similarity_search(query, k=5)
    return [item.page_content for item in results]


def generate_root_cause(test_name: str, similar_failures: list, context: dict):
    prompt = PromptTemplate(
        input_variables=['test_name', 'similar_failures', 'context'],
        template=(
            'You are an AI root cause analyst for CI/CD test reports.\n'
            'Test: {test_name}\n'
            'Context: {context}\n'
            'Similar failures: {similar_failures}\n'
            'Provide a concise root cause, evidence summary, confidence, and recommendation.'
        ),
    )
    prompt_text = prompt.format(
        test_name=test_name,
        similar_failures='; '.join(similar_failures),
        context=context,
    )
    client = ChatOpenAI(model=MODEL_NAME, api_key=os.getenv('OPENAI_API_KEY'))
    response = client.invoke(prompt_text)
    content = response.content
    return {
        'root_cause': content,
        'evidence': f'Found {len(similar_failures)} similar historical failures.',
        'confidence': 75.0,
        'recommendation': 'Investigate the similar failure patterns and apply the recommended change.'
    }
