from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ReportUploadRequest(BaseModel):
    source: str
    pipeline: str
    build_number: str
    report_type: str
    timestamp: datetime

class TestResultModel(BaseModel):
    test_name: str
    test_class: str
    module_name: Optional[str]
    status: str
    execution_time: float
    failure_reason: Optional[str]
    stack_trace: Optional[str]
    build_number: str
    timestamp: datetime

class QualityDigestModel(BaseModel):
    total_executions: int
    pass_rate: float
    fail_rate: float
    top_flaky_tests: List[str]
    top_failing_modules: List[str]
    quality_score: float
    ai_commentary: str
    recommendations: List[str]
