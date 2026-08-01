from fastapi import APIRouter
from notification.slack_notifier import send_slack_message
from notification.email_notifier import send_email

router = APIRouter()

@router.post("/notify/slack")
async def notify_slack(message: str):
    result = send_slack_message(message)
    return {'status': 'ok', 'detail': result}

@router.post("/notify/email")
async def notify_email(subject: str, html_body: str, to_address: str = None):
    result = send_email(subject, html_body, to_address)
    return {'status': 'ok', 'detail': result}
