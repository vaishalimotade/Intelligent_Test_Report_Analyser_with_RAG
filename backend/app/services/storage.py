from datetime import datetime
from .database import database
from ..ai_engine.vector_store import index_failure_records

reports_collection = database["reports"]
results_collection = database["test_results"]
quality_digests_collection = database["quality_digests"]

async def persist_report_records(records):
    if not records:
        return 0

    run_id = f"{records[0]['source']}:{records[0]['pipeline']}:{records[0]['build_number']}:{records[0]['timestamp'].isoformat()}"
    report = {
        "source": records[0]["source"],
        "pipeline": records[0]["pipeline"],
        "report_type": records[0].get("report_type", "unknown"),
        "build_number": records[0]["build_number"],
        "timestamp": records[0]["timestamp"],
        "created_at": datetime.utcnow(),
        "run_id": run_id,
    }
    report_id = reports_collection.insert_one(report).inserted_id
    documents = []
    for record in records:
        raw_content = (
            f"Test Name: {record.get('test_name') or 'Unknown test'}\n"
            f"Final Status: {record.get('status') or 'unknown'}\n"
            f"Feature: {record.get('module_name') or 'Unknown feature'}\n"
            f"Error Summary: {record.get('failure_reason') or 'None'}\n"
            f"Stack Traces / Exception Logs: {record.get('stack_trace') or 'None'}"
        )
        documents.append({**record, "report_id": report_id, "run_id": run_id, "raw_content": raw_content})
    insert_result = results_collection.insert_many(documents)
    for document, parent_id in zip(documents, insert_result.inserted_ids):
        document["_id"] = parent_id
    rag_error = None
    try:
        await index_failure_records(documents)
    except Exception as error:
        rag_error = f"RAG indexing skipped: {type(error).__name__}: {error}"
    return len(documents), rag_error
