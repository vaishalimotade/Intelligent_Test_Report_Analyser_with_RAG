from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from datetime import datetime
from typing import List
from app.services.parser import parse_report
from app.services.storage import persist_report_records

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
    inserted = await persist_report_records(records)
    return {"message": "Report ingested successfully", "ingested_records": inserted}
