from datetime import datetime

from app.services.analytics import get_dashboard_metrics
from app.services.database import database
from app.services.failure import get_failure_patterns
from app.services.flaky import analyze_flaky_tests
from app.services.storage import quality_digest_table


async def generate_quality_digest():
    now = datetime.utcnow()
    metrics = await get_dashboard_metrics(days=7)
    top_flaky = await analyze_flaky_tests()
    patterns = await get_failure_patterns()
    top_failing_modules = [item['module_name'] for item in patterns[:5]]
    quality_score = max(0, 100 - metrics['fail_rate'] - len(top_flaky) * 0.5)
    ai_commentary = (
        f"This week saw {metrics['total_executions']} executions with a pass rate of {metrics['pass_rate']:.2f}% and "
        f"a fail rate of {metrics['fail_rate']:.2f}%. Focus on {', '.join(top_failing_modules[:3]) or 'stable areas'} "
        "to reduce recurring issues."
    )
    recommendations = [
        "Re-run flaky tests with isolated environment",
        "Investigate top failing modules and triage root causes",
        "Tune retry and resilience logic for intermittent failures",
    ]
    html_digest = (
        f"<h1>Weekly Quality Digest</h1>"
        f"<p>Total executions: {metrics['total_executions']}</p>"
        f"<p>Pass rate: {metrics['pass_rate']:.2f}%</p>"
        f"<p>Fail rate: {metrics['fail_rate']:.2f}%</p>"
    )
    await database.execute(
        quality_digest_table.insert().values(
            generation_time=now,
            summary=ai_commentary,
            html_digest=html_digest,
            slack_message=ai_commentary,
        )
    )
    return {
        'total_executions': metrics['total_executions'],
        'pass_rate': metrics['pass_rate'],
        'fail_rate': metrics['fail_rate'],
        'top_flaky_tests': [x['test_name'] for x in top_flaky[:5]],
        'top_failing_modules': top_failing_modules[:5],
        'quality_score': round(quality_score, 2),
        'ai_commentary': ai_commentary,
        'recommendations': recommendations,
    }
