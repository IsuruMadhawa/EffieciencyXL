import os
import smtplib
import ssl

from config import config

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

host=config.get("database", "database.host"),

context = ssl.create_default_context()

with smtplib.SMTP(SMTP_SERVER, PORT) as server:
    server.starttls(context=context)
    server.login(EMAIL, PASSWORD)
    message = """\
    Subject: My First Email

    Hello there, this is my first email sent using Python.
    """
    server.sendmail(EMAIL, "sogiho2398@weirby.com", message)
