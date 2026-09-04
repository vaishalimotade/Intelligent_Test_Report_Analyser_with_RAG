import os
from datetime import datetime, timedelta
from .storage import results_collection
from ..ai_engine.rag_pipeline import retrieve_similar_failures, generate_root_cause

async def root_cause_analysis(test_name: str, window_days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=window_days)
    rows = list(results_collection.find({"test_name": test_name, "timestamp": {"$gte": cutoff}}))
    if not rows:
        return {'root_cause': 'No historical data found', 'evidence': '', 'confidence': 0.0, 'recommendation': 'Ingest more reports for this test'}

    recent_examples = [row['failure_reason'] or 'Unknown failure' for row in rows if row['status'] == 'failed']
    context = {'test_name': test_name, 'recent_failures': recent_examples}
    similar = retrieve_similar_failures(test_name, window_days=window_days)
    analysis = generate_root_cause(test_name, similar, context)
    return analysis
