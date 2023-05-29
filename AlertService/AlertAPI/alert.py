
from flask_restx import (
    Resource,
    Namespace,
)

import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


"""
This code is creating a Flask-RestX namespace called "EMAIL" for an email sending API. The namespace
is used to group related resources and define their routes. The name parameter sets the name of the
namespace, and the description parameter provides a brief description of what the namespace does.
namespace for "/alert"
"""
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
    """
    This code defines a Flask-RestX resource called `EmailSender` within the `EMAIL` namespace. The
    resource handles HTTP POST requests to send emails using the `smtplib` library. The `validate`
    method checks that the required keys (`sender`, `receivers`, `text`, and `title`) are present in the
    request data. The `create_message` method generates a MIME message for each receiver, with both
    plain text and HTML versions of the email contents. The `post` method handles the HTTP POST request,
    validates the request data, and sends the email using the `smtplib` library. If the email is sent
    successfully, the method returns a JSON response with a `status` of `True` and a `msg` of
    `"success"`. If there is an error sending the email, the method returns a JSON response with a
    `status` of `False` and a `msg` of `"error sending mail"`.
    """
    @staticmethod
    def validate(data):
        """
        The static method "validate" checks if a dictionary contains the required keys and raises a
        KeyError if any are missing.
        
        :param data: The `data` parameter is a dictionary that contains information about a message,
        including the sender, receivers, text, and title. The `validate` method is a static method that
        checks if all the required keys are present in the dictionary and raises a `KeyError` if any key
        is missing.
        
        :return: The `data` dictionary is being returned if all the keys in the `keys` list are present
        in the `data` dictionary. If any of the keys are missing, a `KeyError` is raised.
        """
        keys = ["sender", "receivers", "text", "title"]

        for k in keys:
            if k not in data:
                raise KeyError

        return data
    
    @staticmethod
    def create_message(data):
        """
        This is a static method that creates and yields email messages in both plain text and HTML
        formats for multiple receivers.
        
        :param data: The `data` parameter is a dictionary that contains the following keys and values:
        어떤 키벨류값 들어있는지 써야함
        """
        for receiver in data["receivers"]:
            text = data["text"]

            message = MIMEMultipart("alternative")
            message["Subject"] = data["title"]
            message["From"] = data["sender"]
            message["To"] = receiver

            message.attach(MIMEText(text, "plain"))

            yield data["sender"], receiver, message

    
    def post(self):
        """
        This function sends an email with a specified title, contents, sender, and receivers using the
        SMTP protocol and returns a success or error message.
        
        :return: a dictionary with two keys: "status" and "msg". If the email is sent successfully,
        "status" is True and "msg" is "success". If there is an error sending the email, "status" is
        False and "msg" is "error sending mail".
        
        ---
        request = {
        title: email title
        text: email contents
        sender: example@example.com
        receivers: [email1@mail.com, email2@mail.com]
        }
        """
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
            }, 200

        except Exception:
            return {
                "status": False,
                "msg": "error sending mail"
            }, 500
            
    
