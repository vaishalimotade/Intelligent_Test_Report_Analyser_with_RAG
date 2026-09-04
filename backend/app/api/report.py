from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from datetime import datetime
from ..services.parser import parse_report
from ..services.storage import persist_report_records

router = APIRouter()

@router.post("/upload-report", response_model=dict)
async def upload_report(
    source: str = Form(...),
    pipeline: str = Form(...),
    build_number: str = Form(...),
    report_type: str = Form(...),
    timestamp: datetime = Form(...),
    file: UploadFile = File(...),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded report file is empty")

    records = parse_report(content.decode("utf-8"), report_type, source, pipeline, build_number, timestamp)
    for record in records:
        record["report_type"] = report_type
    inserted, rag_error = await persist_report_records(records)
    result = {"message": "Report ingested successfully", "ingested_records": inserted}
    if rag_error:
        result["warning"] = rag_error
    return result
