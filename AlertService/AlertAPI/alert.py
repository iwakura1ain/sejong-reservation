
from flask_restx import (
    Resource,
    Namespace,
)

import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# namespace for "/alert"
EMAIL = Namespace(
    name="email",
    description="사용자에게 이메일을 보내는 API",
)

def validate(data):
    keys = ["sender", "receiver", "text", "title"]

    for k in keys:
        if k not in data:
            raise KeyError

    return data

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "ernie937@gmail.com"
receiver_email = "ernie937@gmail.com"
password = "gwlvstkadqhqelix"

with open("mail-format.html", mode="r") as f:
    mail_format = f.read()


@EMAIL.route('')
class EmailSender(Resource):
    def post(self):
        """
        {
        sender:
        receiver:
        text:
        }
        """

        from flask import request
        
        try:
            req = validate(request.json)

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                for receiver in req["receiver"]:
                    html = mail_format.format(text=req["text"])
                    text = req["text"]

                    message = MIMEMultipart("alternative")
                    message["Subject"] = req["title"]
                    message["From"] = req["sender"]
                    message["To"] = receiver
                    message.attach(MIMEText(text, "plain"))
                    message.attach(MIMEText(html, "html"))

                    server.starttls(context=context)
                    server.login(req["sender"], password)
                    server.sendmail(req["sender"], receiver, message.as_string())

            return {
                "status": True,
                "msg": "sucess"
            }

        except:
            return {
                "status": False,
                "msg": "error sending mail"
            }
            
    
