import os
from datetime import datetime, timedelta
from app.services.database import database
from app.services.storage import result_table
from app.ai_engine.rag_pipeline import retrieve_similar_failures, generate_root_cause

async def root_cause_analysis(test_name: str):
    query = result_table.select().where(result_table.c.test_name == test_name)
    rows = await database.fetch_all(query)
    if not rows:
        return {'root_cause': 'No historical data found', 'evidence': '', 'confidence': 0.0, 'recommendation': 'Ingest more reports for this test'}

    recent_examples = [row['failure_reason'] or 'Unknown failure' for row in rows if row['status'] == 'failed']
    context = {'test_name': test_name, 'recent_failures': recent_examples}
    similar = retrieve_similar_failures(test_name)
    analysis = generate_root_cause(test_name, similar, context)
    return analysis
