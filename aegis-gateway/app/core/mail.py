from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr,NameEmail

from app.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = settings.USE_CREDENTIALS,
    VALIDATE_CERTS = settings.VALIDATE_CERTS
)


async def send_mail(email:EmailStr,token:str)->None:
  """ send a password reset-link to the user mail."""
  reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
  html_body = f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #222;">
        <h2>Password Reset Request</h2>
        <p>You recently requested to reset your password. Click the button below to complete the process:</p>
        <p style="margin: 25px 0;">
          <a href="{reset_link}" 
            style="background-color: #2563eb; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
            Reset Password
          </a>
        </p>
        <p>Or paste this link into your browser:</p>
        <p style="word-break: break-all; color: #2563eb;">{reset_link}</p>
        <p style="color: #666; font-size: 0.9em; margin-top: 30px;">
          This link will expire in 15 minutes. If you did not make this request, you can safely ignore this email.
        </p>
      </body>
    </html>
    """

  message = MessageSchema(
        subject="Reset-Password Request",
        recipients=[NameEmail(name="",email=email)],
        body=html_body,
        subtype=MessageType.html)

  fm=FastMail(conf)
  await fm.send_message(message)