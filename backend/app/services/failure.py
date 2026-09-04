from .storage import results_collection
from collections import Counter

async def get_failure_patterns():
    rows = list(results_collection.find({"status": "failed"}))
    counter = Counter()
    for row in rows:
        reason = row['failure_reason'] or 'Unknown failure'
        module = row['module_name'] or 'Unknown module'
        counter[(reason, module)] += 1

    return [
        {
            'reason': reason,
            'module_name': module,
            'count': count,
            'first_seen': None,
            'last_seen': None,
        }
        for (reason, module), count in counter.most_common(25)
    ]
