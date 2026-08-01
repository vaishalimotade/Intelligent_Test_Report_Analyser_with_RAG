from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.llm import LLMService

router = APIRouter()


class LLMRequest(BaseModel):
    context: str = Field(..., min_length=1)
    system_prompt: str | None = None
    user_template: str | None = None


@router.post("/llm/analyze")
async def analyze_with_llm(payload: LLMRequest):
    service = LLMService()
    try:
        return service.generate_text(
            context=payload.context,
            system_prompt=payload.system_prompt,
            user_template=payload.user_template,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
