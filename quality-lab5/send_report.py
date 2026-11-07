import os
import smtplib
import ssl
from email.message import EmailMessage

sender = os.environ["MAIL_USERNAME"]
password = os.environ["MAIL_PASSWORD"]
recipient = os.environ["MAIL_TO"]

subject = os.environ["REPORT_SUBJECT"]
body = os.environ["REPORT_BODY"]

message = EmailMessage()
message["From"] = sender
message["To"] = recipient
message["Subject"] = subject
message.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as smtp:
    smtp.login(sender, password)
    smtp.send_message(message)

print("Отчёт успешно отправлен!")
