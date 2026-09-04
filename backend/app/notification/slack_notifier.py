import os
import ssl

import httpx
import truststore


def _get_ssl_context():
    ca_file = os.getenv("SSL_CERT_FILE")
    if ca_file:
        return ssl.create_default_context(cafile=ca_file)
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

def send_slack_message(message: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL is not configured")
    response = httpx.post(
        webhook_url,
        json={"text": message},
        timeout=10.0,
        verify=_get_ssl_context(),
    )
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"status": response.text}
