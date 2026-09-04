import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.report import router as report_router
from .api.analysis import router as analysis_router
from .api.notification import router as notification_router
from .api.llm import router as llm_router
from .services.database import init_db
from .services.scheduler import weekly_digest_loop

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


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    await init_db()
    app.state.digest_stop_event = asyncio.Event()
    app.state.digest_task = asyncio.create_task(weekly_digest_loop(app.state.digest_stop_event))


@app.on_event("shutdown")
async def shutdown_event():
    stop_event = getattr(app.state, "digest_stop_event", None)
    digest_task = getattr(app.state, "digest_task", None)
    if stop_event:
        stop_event.set()
    if digest_task:
        await digest_task

app.include_router(report_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(llm_router, prefix="/api")
