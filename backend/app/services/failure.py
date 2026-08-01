from app.services.database import database
from app.services.storage import result_table
from collections import Counter

async def get_failure_patterns():
    query = result_table.select().where(result_table.c.status == 'failed')
    rows = await database.fetch_all(query)
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
