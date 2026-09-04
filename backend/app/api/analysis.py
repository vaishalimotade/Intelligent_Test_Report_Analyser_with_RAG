from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Query

from ..services.analytics import get_dashboard_metrics
from ..services.flaky import analyze_flaky_tests
from ..services.failure import get_failure_patterns
from ..services.heatmap import get_heatmap_data
from ..services.quality import generate_quality_digest
from ..services.root_cause import root_cause_analysis
from ..services.overview import get_overview

router = APIRouter()

@router.get("/overview")
async def overview(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    pipeline: Optional[str] = None,
    feature: Optional[str] = None,
):
    end_date = end_date or date.today()
    start_date = start_date or end_date - timedelta(days=30)
    return await get_overview(start_date, end_date, pipeline, feature)

@router.get("/flaky-tests")
async def get_flaky_tests():
    return await analyze_flaky_tests()

@router.get("/failure-patterns")
async def failure_patterns():
    return await get_failure_patterns()

@router.get("/root-cause/{test_name}")
async def root_cause(test_name: str, window_days: int = Query(default=30, ge=1, le=3650)):
    return await root_cause_analysis(test_name, window_days)

@router.get("/quality-digest")
async def quality_digest():
    return await generate_quality_digest()

@router.get("/heatmap")
async def heatmap(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    pipeline: Optional[str] = None,
):
    return await get_heatmap_data(start_date, end_date, pipeline)

@router.get("/dashboard-stats")
async def dashboard_stats():
    metrics = await get_dashboard_metrics(days=7)
    metrics['top_flaky_tests'] = await analyze_flaky_tests()
    return metrics
