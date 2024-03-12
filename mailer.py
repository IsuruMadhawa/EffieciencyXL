import smtplib
import ssl

from config import config

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL = config.get("mailer", "mailer.email")
PASSWORD = config.get("mailer", "mailer.password")

context = ssl.create_default_context()


def send_mail(recipient: str, message: str):
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, recipient, message)
