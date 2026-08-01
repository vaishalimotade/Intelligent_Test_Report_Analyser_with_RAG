import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv('EMAIL_SMTP_HOST')
SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
SMTP_USER = os.getenv('EMAIL_SMTP_USER')
SMTP_PASSWORD = os.getenv('EMAIL_SMTP_PASSWORD')
FROM_EMAIL = os.getenv('NOTIFICATION_FROM_EMAIL')
ADMIN_EMAIL = os.getenv('NOTIFICATION_ADMIN_EMAIL')


def send_email(subject: str, html_body: str, to_address: str = None):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL]):
        raise ValueError('Email configuration is incomplete')
    recipient = to_address or ADMIN_EMAIL
    if not recipient:
        raise ValueError('Notification recipient is not configured')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = recipient
    msg.attach(MIMEText(html_body, 'html'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, recipient, msg.as_string())

    return {'status': 'sent', 'recipient': recipient}
