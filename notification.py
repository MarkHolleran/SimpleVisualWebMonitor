import smtplib
from email.mime.text import MIMEText
import json

credentials = json.load(open('credentials.json'))


def send_email(*links):
    sender = credentials["sender"]
    password = credentials["password"]
    recipients = credentials["recipients"]
    subject = credentials["subject"]
    body = credentials["body"]

    for link in links:
        body = body + (str(link) + '\n\n')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    s.login(sender, password)

    s.sendmail(sender, recipients, msg.as_string())
    print("Alert sent!")
