from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.report import router as report_router
from app.api.analysis import router as analysis_router
from app.api.notification import router as notification_router
from app.api.llm import router as llm_router
from app.services.database import init_db

app = FastAPI(
    title="Intelligent Test Report Analyzer & Insights Engine",
    description="LLM-powered quality analytics platform for CI/CD test reports.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(report_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(llm_router, prefix="/api")
