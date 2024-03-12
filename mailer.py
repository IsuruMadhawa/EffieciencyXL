import os
import smtplib
import ssl

from config import config

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL = config.get("mailer", "mailer.email")
PASSWORD = config.get("mailer", "mailer.password")

context = ssl.create_default_context()

with smtplib.SMTP(SMTP_SERVER, PORT) as server:
    server.starttls(context=context)
    server.login(EMAIL, PASSWORD)
    message = """\
    Subject: My First Email

    Hello there, this is my first email sent using Python.
    """
    server.sendmail(EMAIL, "sogiho2398@weirby.com", message)
