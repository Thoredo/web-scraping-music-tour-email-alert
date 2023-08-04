import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
SENDER = os.getenv("MY_EMAIL")
RECEIVER = os.getenv("MY_EMAIL")


def send_email(message):
    """ Sents email to gmail adress"""
    host = "smtp.gmail.com"
    port = 485

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, message)