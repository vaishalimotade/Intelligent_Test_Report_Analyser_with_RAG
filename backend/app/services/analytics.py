from datetime import datetime, timedelta
from typing import Any, Dict, List

from app.services.database import database
from app.services.storage import result_table


async def get_dashboard_metrics(days: int = 7) -> Dict[str, Any]:
    now = datetime.utcnow()
    window = now - timedelta(days=days)
    query = result_table.select().where(result_table.c.timestamp >= window)
    rows = await database.fetch_all(query)

    if not rows:
        return {
            'total_executions': 0,
            'pass_rate': 0.0,
            'fail_rate': 0.0,
        }

    total = len(rows)
    passed = sum(1 for row in rows if row['status'] == 'passed')
    failed = sum(1 for row in rows if row['status'] == 'failed')
    return {
        'total_executions': total,
        'pass_rate': round((passed / total * 100) if total else 0.0, 2),
        'fail_rate': round((failed / total * 100) if total else 0.0, 2),
    }
