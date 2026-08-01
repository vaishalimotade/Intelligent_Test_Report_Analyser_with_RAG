from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UploadReportResponse(BaseModel):
    message: str
    ingested_records: int

class FlakyTestResponse(BaseModel):
    test_name: str
    test_class: str
    module_name: Optional[str]
    flaky_score: float
    risk_level: str
    confidence_score: float

class FailurePatternResponse(BaseModel):
    reason: str
    count: int
    module_name: Optional[str]
    first_seen: datetime
    last_seen: datetime

class RootCauseResponse(BaseModel):
    root_cause: str
    evidence: str
    confidence: float
    recommendation: str

class QualityDigestResponse(BaseModel):
    html_digest: str
    pdf_digest: bytes
    summary: str
