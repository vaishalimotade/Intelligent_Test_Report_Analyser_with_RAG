from app.services.database import database
from app.services.storage import result_table
from statistics import mean, stdev

RISK_LEVELS = [
    (20, 'Low'),
    (40, 'Medium'),
    (70, 'High'),
    (100, 'Critical'),
]

async def analyze_flaky_tests():
    query = result_table.select()
    rows = await database.fetch_all(query)
    if not rows:
        return []

    tests = {}
    for row in rows:
        key = (row['test_name'], row['test_class'], row['module_name'])
        stats = tests.setdefault(key, {'total': 0, 'failed': 0, 'execution_times': []})
        stats['total'] += 1
        if row['status'] == 'failed':
            stats['failed'] += 1
        stats['execution_times'].append(row['execution_time'])

    result = []
    for (test_name, test_class, module_name), stats in tests.items():
        total = stats['total']
        failures = stats['failed']
        flaky_score = (failures / total) * 100 if total else 0
        risk_level = next(label for threshold, label in RISK_LEVELS if flaky_score <= threshold)
        confidence_score = 100 - min(100, abs(mean(stats['execution_times']) - mean(stats['execution_times'])) if len(stats['execution_times']) > 1 else 0)
        result.append({
            'test_name': test_name,
            'test_class': test_class,
            'module_name': module_name,
            'flaky_score': round(flaky_score, 2),
            'risk_level': risk_level,
            'confidence_score': round(confidence_score, 2),
        })
    return sorted(result, key=lambda x: x['flaky_score'], reverse=True)
