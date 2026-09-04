import asyncio
import logging
import os

from ..notification.email_notifier import send_email
from ..notification.slack_notifier import send_slack_message
from .quality import generate_quality_digest

logger = logging.getLogger(__name__)


async def deliver_weekly_digest() -> None:
    digest = await generate_quality_digest()
    slack_enabled = os.getenv("WEEKLY_DIGEST_SLACK_ENABLED", "true").lower() == "true"
    email_enabled = os.getenv("WEEKLY_DIGEST_EMAIL_ENABLED", "false").lower() == "true"

    if slack_enabled and os.getenv("SLACK_WEBHOOK_URL"):
        await asyncio.to_thread(send_slack_message, digest["slack_message"])
    if email_enabled:
        await asyncio.to_thread(
            send_email,
            "Weekly Test Quality Digest",
            digest["html_digest"],
            os.getenv("NOTIFICATION_ADMIN_EMAIL"),
        )


async def weekly_digest_loop(stop_event: asyncio.Event) -> None:
    interval = int(os.getenv("WEEKLY_DIGEST_INTERVAL_SECONDS", "604800"))
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval)
        except asyncio.TimeoutError:
            try:
                await deliver_weekly_digest()
            except Exception:
                logger.exception("Weekly digest delivery failed")
