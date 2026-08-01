from collections import Counter
from datetime import datetime, timedelta
from app.services.database import database
from app.services.storage import result_table

async def get_heatmap_data():
    now = datetime.utcnow()
    window = now - timedelta(days=30)
    query = result_table.select().where(result_table.c.timestamp >= window)
    rows = await database.fetch_all(query)
    module_counts = Counter()
    module_failures = Counter()
    for row in rows:
        module = row['module_name'] or 'Unknown'
        module_counts[module] += 1
        if row['status'] == 'failed':
            module_failures[module] += 1
    heatmap = []
    for module in module_counts:
        failure_rate = module_failures[module] / module_counts[module] * 100 if module_counts[module] else 0
        risk = 'Green'
        if failure_rate > 70:
            risk = 'Red'
        elif failure_rate > 40:
            risk = 'Orange'
        elif failure_rate > 20:
            risk = 'Yellow'
        heatmap.append({
            'module_name': module,
            'failure_density': module_failures[module],
            'failure_frequency': module_counts[module],
            'risk_score': failure_rate,
            'trend': 'increasing' if failure_rate > 20 else 'stable',
            'color': risk,
        })
    return sorted(heatmap, key=lambda item: item['risk_score'], reverse=True)
