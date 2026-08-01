import os
import httpx

WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')


def send_slack_message(message: str):
    if not WEBHOOK_URL:
        raise ValueError('SLACK_WEBHOOK_URL is not configured')
    payload = {'text': message}
    response = httpx.post(WEBHOOK_URL, json=payload, timeout=10.0)
    response.raise_for_status()
    return response.json()
