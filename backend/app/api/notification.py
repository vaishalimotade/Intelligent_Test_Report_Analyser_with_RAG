import httpx
from fastapi import APIRouter, HTTPException
from ..notification.slack_notifier import send_slack_message
from ..notification.email_notifier import send_email

router = APIRouter()

@router.post("/notify/slack")
async def notify_slack(message: str):
    try:
        result = send_slack_message(message)
        return {'status': 'ok', 'detail': result}
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except httpx.HTTPStatusError as error:
        response_text = error.response.text.strip() or "Slack rejected the notification"
        raise HTTPException(status_code=502, detail=response_text) from error
    except httpx.RequestError as error:
        raise HTTPException(status_code=502, detail=f"Slack connection failed: {error}") from error

@router.post("/notify/email")
async def notify_email(subject: str, html_body: str, to_address: str = None):
    result = send_email(subject, html_body, to_address)
    return {'status': 'ok', 'detail': result}
