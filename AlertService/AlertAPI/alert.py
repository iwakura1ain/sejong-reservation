
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

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
password = "gwlvstkadqhqelix"

with open("mail-format.html", mode="r") as f:
    mail_format = f.read()


@EMAIL.route('')
class EmailSender(Resource):
    @staticmethod
    def validate(data):
        keys = ["sender", "receivers", "text", "title"]

        for k in keys:
            if k not in data:
                raise KeyError

        return data
    
    @staticmethod
    def create_message(data):
        for receiver in data["receivers"]:
            html = mail_format.format(text=data["text"])
            text = data["text"]

            message = MIMEMultipart("alternative")
            message["Subject"] = data["title"]
            message["From"] = data["sender"]
            message["To"] = receiver

            message.attach(MIMEText(text, "plain"))
            message.attach(MIMEText(html, "html"))

            yield data["sender"], data["receiver"], message

    
    def post(self):
        from flask import request

        try:
            req = self.validate(request.json)

            with smtplib.SMTP(smtp_server, port) as server:
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.login(req["sender"], password)
                
                for sender, receiver, message in self.create_message(req):
                    server.sendmail(sender, receiver, message.as_string())

            return {
                "status": True,
                "msg": "sucess"
            }

        except:
            return {
                "status": False,
                "msg": "error sending mail"
            }
            
    
