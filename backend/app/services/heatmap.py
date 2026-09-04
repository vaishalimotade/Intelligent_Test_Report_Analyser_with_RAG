from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Optional
from .storage import results_collection

async def get_heatmap_data(start_date: Optional[date] = None, end_date: Optional[date] = None, pipeline: Optional[str] = None):
    end_date = end_date or datetime.utcnow().date()
    start_date = start_date or end_date - timedelta(days=29)
    query = {"timestamp": {"$gte": datetime.combine(start_date, datetime.min.time()), "$lt": datetime.combine(end_date + timedelta(days=1), datetime.min.time())}}
    if pipeline:
        query["pipeline"] = pipeline
    rows = list(results_collection.find(query))
    buckets = defaultdict(lambda: {"executions": 0, "failures": 0})
    for row in rows:
        module = row['module_name'] or 'Unknown'
        timestamp = row.get("timestamp")
        day = timestamp.date().isoformat() if hasattr(timestamp, "date") else str(timestamp)[:10]
        bucket = buckets[(day, module)]
        bucket["executions"] += 1
        if row['status'] == 'failed':
            bucket["failures"] += 1
    return [
        {
            "date": day,
            "module_name": module,
            "failure_density": values["failures"],
            "failure_frequency": values["executions"],
            "risk_score": round(values["failures"] / values["executions"] * 100, 2) if values["executions"] else 0,
        }
        for (day, module), values in sorted(buckets.items())
    ]
