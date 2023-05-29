from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

from flask_jwt_extended import jwt_required as jwt_required_original

from functools import wraps
import json



def retrieve_jwt():
    try:
        verify_jwt_in_request()
        return get_jwt()["sub"]

    except Exception as e:
        print(e)
        return None

def serialize(data, include=[], exclude=[]):
    retval = {}
    if len(include) != 0:
        for key in include:
            retval[key] = data[key]
        return retval

    for key, item in data.items():
        if key not in exclude:
            retval[key] = item
    return retval


def protected():
    """
    decorator which protects endpoints that require authorization
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            identity = retrieve_jwt()
            if identity["type"] == 1 or identity["id"] == kwargs.get("id"):
                return fn(*args, **kwargs)
            
            return {
                "status": False,
                "msg": "unauthorized"
            }, 200
            
        return decorator
    return wrapper

def admin_only():
    """
    decorator which protects endpoints that require authorization
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            identity = retrieve_jwt()
            if identity["type"] == 1:
                return fn(*args, **kwargs)
            
            return {
                "status": False,
                "msg": "unauthorized"
            }, 200
            
        return decorator
    return wrapper

def create_register_confirmation_email(
    user, sender,
    title="[회의실 예약 시스템] 회원가입이 완료되었습니다.",
    template_name="template.txt"
):
    """
    Generates an alert email for when new user is registered.
    sender: email address that sends out alert emails
    title: email title
    template_name: email body template file name

    Returns a dict for POST alertservice/alert body
    """
    from config import dept_str, user_type_str

    # email receiver
    receivers = [user["email"]]

    template_data = {
        "user_id":user["id"],
        "name":user["name"],
        "dept":dept_str[user["dept"]],
        "phone":user["phone"],
        "email":user["email"],
        "type":user_type_str[user["type"]],
    }

    with open(template_name, "r") as f:
        template = f.read()

    return {
        "title": title,
        "text": template.format(**template_data),
        "sender": sender,
        "receivers": receivers
    }
