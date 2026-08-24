import os
import smtplib
from email.message import EmailMessage

from celery import Celery

app = Celery('email', broker='redis://localhost:6379/0')

@app.task
def send_mail(receiver_mail , otp_code):
    sender = os.environ["EMAIL_HOST_USER"]
    password = os.environ["EMAIL_HOST_PASSWORD"]
    receiver = receiver_mail
    msg = EmailMessage()
    msg["Subject"] = "Test OTP CODE"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(f"code : {otp_code}")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
