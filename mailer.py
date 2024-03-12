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
    Your clearance request has been approved. Please visit the nearest police station to collect your clearance report.
    """
    server.sendmail(EMAIL, "sogiho2398@weirby.com", message)
