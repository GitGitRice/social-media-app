import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlencode

from dotenv import load_dotenv

from web_app.auth import create_public_post_access_token

load_dotenv()


def email_notifications_enabled() -> bool:
    """
    Returns True if email notifications should be sent.
    """
    return os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "false").lower() == "true"


def build_post_link(post_id: int) -> str:
    """
    Builds an absolute link to the public post detail page.
    """
    app_base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    token = create_public_post_access_token(post_id)
    query = urlencode({"token": token})
    return f"{app_base_url}/static/post.html?{query}"


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends a plain text email through the configured SMTP server.

    Returns True if the email was sent, False if email notifications are disabled
    or the SMTP configuration is incomplete.
    """
    if not email_notifications_enabled():
        return False

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_host or not smtp_from:
        return False

    message = EmailMessage()
    message["From"] = smtp_from
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            if smtp_use_tls:
                smtp.starttls()
            if smtp_username and smtp_password:
                smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def send_comment_notification(to_email: str, post_id: int, commenter_name: str) -> bool:
    """
    Sends an email notification for a new comment on a post.
    """
    post_link = build_post_link(post_id)
    subject = "New comment on your post"
    body = (
        f"{commenter_name} commented on your post.\n\n"
        f"Open the post here:\n{post_link}"
    )
    return send_email(to_email, subject, body)


def send_new_post_notification(to_email: str, post_id: int, author_name: str) -> bool:
    """
    Sends an email notification for a new post from a followed user.
    """
    post_link = build_post_link(post_id)
    subject = f"{author_name} created a new post"
    body = (
        f"{author_name} created a new post.\n\n"
        f"Open the post here:\n{post_link}"
    )
    return send_email(to_email, subject, body)


def send_like_notification(to_email: str, post_id: int, liker_name: str) -> bool:
    """
    Sends an email notification for a new like on a post.
    """
    post_link = build_post_link(post_id)
    subject = "New like on your post"
    body = (
        f"{liker_name} liked your post.\n\n"
        f"Open the post here:\n{post_link}"
    )
    return send_email(to_email, subject, body)
