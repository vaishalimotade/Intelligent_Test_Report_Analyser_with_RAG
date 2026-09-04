from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional

from .storage import results_collection


def _error_category(reason: str) -> str:
    text = reason.lower()
    categories = (
        ("Timeout", ("timeout", "timed out", "time out")),
        ("Authentication", ("auth", "login", "password", "unauthorized", "forbidden")),
        ("Database", ("database", "db", "sql", "mongo", "query")),
        ("Network", ("network", "connection", "socket", "http", "503", "502")),
        ("Assertion", ("assert", "expected", "actual")),
    )
    for category, keywords in categories:
        if any(keyword in text for keyword in keywords):
            return category
    return "Other"


async def get_overview(
    start_date: date,
    end_date: date,
    pipeline: Optional[str] = None,
    feature: Optional[str] = None,
) -> Dict[str, Any]:
    query: Dict[str, Any] = {
        "timestamp": {"$gte": datetime.combine(start_date, datetime.min.time()), "$lt": datetime.combine(end_date + timedelta(days=1), datetime.min.time())}
    }
    if pipeline:
        query["pipeline"] = pipeline
    if feature:
        query["module_name"] = feature

    rows = list(results_collection.find(query))
    total_executions = len(rows)
    passed_executions = sum(row.get("status") == "passed" for row in rows)
    failed_executions = sum(row.get("status") == "failed" for row in rows)
    skipped_executions = total_executions - passed_executions - failed_executions
    unique_tests = {(row.get("test_name"), row.get("test_class"), row.get("module_name")) for row in rows}
    runs = defaultdict(list)
    for row in rows:
        run_key = (row.get("pipeline") or "Unknown pipeline", row.get("build_number") or "Unknown build")
        runs[run_key].append(row)
    passed_runs = sum(any(row.get("status") == "passed" for row in run_rows) and not any(row.get("status") == "failed" for row in run_rows) for run_rows in runs.values())
    failed_runs = sum(any(row.get("status") == "failed" for row in run_rows) for run_rows in runs.values())

    feature_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "skipped": 0})
    error_stats = defaultdict(lambda: {"count": 0, "test_cases": set(), "runs": set(), "examples": []})
    hotspot_stats = defaultdict(lambda: {"tests": set(), "failed_tests": set()})
    flaky_stats = defaultdict(lambda: {"runs": set(), "passed_runs": set(), "failed_runs": set()})

    for row in rows:
        module = row.get("module_name") or "Unknown feature"
        status = row.get("status", "unknown")
        feature_stats[module][status if status in ("passed", "failed", "skipped") else "skipped"] += 1
        test_key = (row.get("test_name") or "Unknown test", row.get("test_class"), module)
        hotspot_stats[module]["tests"].add(test_key)
        if status == "failed":
            hotspot_stats[module]["failed_tests"].add(test_key)
            reason = row.get("failure_reason") or "Unknown failure"
            category = _error_category(reason)
            error = error_stats[category]
            error["count"] += 1
            error["test_cases"].add(row.get("test_name") or "Unknown test")
            error["runs"].add(f"{row.get('pipeline', 'unknown')} / {row.get('build_number', 'unknown')}")
            if reason not in error["examples"] and len(error["examples"]) < 5:
                error["examples"].append(reason)
        key = (row.get("test_name") or "Unknown test", module)
        run_key = (row.get("pipeline") or "Unknown pipeline", row.get("build_number") or "Unknown build")
        flaky_stats[key]["runs"].add(run_key)
        if status == "failed":
            flaky_stats[key]["failed_runs"].add(run_key)
        elif status == "passed":
            flaky_stats[key]["passed_runs"].add(run_key)

    features = []
    for module, stats in feature_stats.items():
        features.append({"feature": module, "passed": stats["passed"], "failed": stats["failed"], "skipped": stats["skipped"], "total": sum(stats.values())})
    features.sort(key=lambda item: item["total"], reverse=True)

    error_categories = []
    for category, error in sorted(error_stats.items(), key=lambda item: item[1]["count"], reverse=True):
        error_categories.append({
            "category": category,
            "occurrences": error["count"],
            "test_case_count": len(error["test_cases"]),
            "run_count": len(error["runs"]),
            "test_cases": sorted(error["test_cases"]),
            "runs": sorted(error["runs"]),
            "examples": error["examples"],
        })

    hotspots = []
    for module, stats in sorted(hotspot_stats.items(), key=lambda item: len(item[1]["failed_tests"]), reverse=True):
        hotspots.append({
            "feature": module,
            "failed_tests": len(stats["failed_tests"]),
            "total_tests": len(stats["tests"]),
            "failure_rate": round(len(stats["failed_tests"]) / len(stats["tests"]) * 100, 2) if stats["tests"] else 0,
        })

    flaky_tests = []
    for (test_name, module), stats in sorted(flaky_stats.items(), key=lambda item: len(item[1]["failed_runs"]), reverse=True):
        total_runs = len(stats["runs"])
        failed_runs_for_test = len(stats["failed_runs"])
        is_flaky = len(stats["passed_runs"]) > 0 and failed_runs_for_test > 0 and total_runs >= 2
        if is_flaky:
            flaky_tests.append({"test_name": test_name, "feature": module, "flaky_score": round(failed_runs_for_test / total_runs * 100, 2), "runs": total_runs})

    return {
        "summary": {
            "total_executions": total_executions,
            "passed_executions": passed_executions,
            "failed_executions": failed_executions,
            "skipped_executions": skipped_executions,
            "unique_test_cases": len(unique_tests),
            "run_count": len(runs),
            "passed_runs": passed_runs,
            "failed_runs": failed_runs,
            "pass_rate": round(passed_executions / total_executions * 100, 2) if total_executions else 0,
            "fail_rate": round(failed_executions / total_executions * 100, 2) if total_executions else 0,
        },
        "features": features,
        "error_categories": error_categories,
        "hotspots": hotspots,
        "flaky_tests": flaky_tests[:25],
    }