from fastapi import APIRouter

from app.services.analytics import get_dashboard_metrics
from app.services.flaky import analyze_flaky_tests
from app.services.failure import get_failure_patterns
from app.services.heatmap import get_heatmap_data
from app.services.quality import generate_quality_digest
from app.services.root_cause import root_cause_analysis

router = APIRouter()

@router.get("/flaky-tests")
async def get_flaky_tests():
    return await analyze_flaky_tests()

@router.get("/failure-patterns")
async def failure_patterns():
    return await get_failure_patterns()

@router.get("/root-cause/{test_name}")
async def root_cause(test_name: str):
    return await root_cause_analysis(test_name)

@router.get("/quality-digest")
async def quality_digest():
    return await generate_quality_digest()

@router.get("/heatmap")
async def heatmap():
    return await get_heatmap_data()

@router.get("/dashboard-stats")
async def dashboard_stats():
    metrics = await get_dashboard_metrics(days=7)
    metrics['top_flaky_tests'] = await analyze_flaky_tests()
    return metrics
