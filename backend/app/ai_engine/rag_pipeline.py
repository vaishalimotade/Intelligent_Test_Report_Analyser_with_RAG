import os
import json
from datetime import datetime, timedelta
from bson import ObjectId

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from .vector_store import get_vector_store
from ..services.storage import results_collection

MODEL_NAME = os.getenv("MODEL_NAME") or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")


def retrieve_similar_failures(test_name: str, window_days: int = 30):
    vector_store = get_vector_store()
    query = f"Find similar failures for {test_name}"
    results = vector_store.similarity_search(query, k=20)
    cutoff = datetime.utcnow() - timedelta(days=window_days)
    failures = []
    seen_parents = set()
    for item in results:
        parent_ids = json.loads(item.metadata.get("mongo_ids", "[]"))
        if not parent_ids and item.metadata.get("mongo_id"):
            parent_ids = [item.metadata["mongo_id"]]
        for parent_id in parent_ids:
            if parent_id in seen_parents:
                continue
            try:
                parent = results_collection.find_one({"_id": ObjectId(parent_id)})
            except Exception:
                parent = None
            if parent:
                timestamp = parent.get("timestamp")
                if isinstance(timestamp, datetime) and timestamp < cutoff:
                    continue
                failures.append(
                    "Full historical test result:\n"
                    f"Test: {parent.get('test_name')}\n"
                    f"Status: {parent.get('status')}\n"
                    f"Failure: {parent.get('failure_reason') or 'Unknown failure'}\n"
                    f"Stack trace: {parent.get('stack_trace') or 'Not available'}"
                )
                seen_parents.add(parent_id)
    return failures


def generate_root_cause(test_name: str, similar_failures: list, context: dict):
    prompt = PromptTemplate(
        input_variables=["test_name", "similar_failures", "context"],
        template=(
            "You are an AI root cause analyst for CI/CD test reports.\n"
            "Test: {test_name}\n"
            "Context: {context}\n"
            "Similar failures: {similar_failures}\n"
            "Provide a concise root cause, evidence summary, confidence, and recommendation."
        ),
    )
    prompt_text = prompt.format(
        test_name=test_name,
        similar_failures="; ".join(similar_failures),
        context=context,
    )
    client = ChatOpenAI(model=MODEL_NAME, api_key=os.getenv("OPENAI_API_KEY"), base_url=BASE_URL)
    response = client.invoke(prompt_text)
    return {
        "root_cause": response.content,
        "evidence": f"Found {len(similar_failures)} similar historical failures.",
        "confidence": 75.0,
        "recommendation": "Investigate the similar failure patterns and apply the recommended change.",
    }
