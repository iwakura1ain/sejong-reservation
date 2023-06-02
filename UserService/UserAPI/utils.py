from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

from flask_jwt_extended import jwt_required as jwt_required_original

from functools import wraps
import json



def retrieve_jwt():
    """
    This function attempts to retrieve a JSON Web Token (JWT) from a request and returns the "sub" claim
    if successful, otherwise it returns None and prints the error message.
    :return: the value of the "sub" claim in the JSON Web Token (JWT) retrieved from the request, if the
    token is verified successfully. If there is an exception, the function prints the error message and
    returns None.
    """
    try:
        verify_jwt_in_request()
        return get_jwt()["sub"]

    except Exception as e:
        print(e)
        return None

def serialize(data, include=[], exclude=[]):
    """
    The function "serialize" takes in data and returns a dictionary with specified keys included or
    excluded.
    
    :param data: The data parameter is a dictionary containing the data that needs to be serialized
    :param include: A list of keys that should be included in the serialized output. If this parameter
    is not empty, only the keys specified in the list will be included in the output
    :param exclude: The `exclude` parameter is a list of keys that should be excluded from the
    serialized output. If a key in the `exclude` list is found in the `data` dictionary, it will not be
    included in the returned `retval`
    :return: The function `serialize` returns a dictionary containing a subset of the input `data`
    dictionary, based on the `include` and `exclude` parameters. If `include` is not empty, only the
    keys specified in `include` are included in the output dictionary. If `exclude` is not empty, the
    keys specified in `exclude` are excluded from the output dictionary. If both `include
    """
    retval = {}
    if len(include) != 0:
        for key in include:
            retval[key] = data[key]
        return retval

    for key, item in data.items():
        if key not in exclude:
            retval[key] = item
    return retval

# decorator which protects endpoints that require authorization
def protected():
    """
    This is a Python decorator function that protects endpoints requiring authorization by checking the
    identity of the user.
    :return: The `protected()` function returns a decorator function `wrapper()`, which in turn returns
    a decorated function `decorator()`. The decorated function `decorator()` checks if the user is
    authorized to access the endpoint by retrieving the JWT token and checking the identity type and ID.
    If the user is authorized, it calls the original function `fn(*args, **kwargs)` and returns its
    result. If
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

# decorator which protects endpoints that require authorization
def admin_only():
    """
    This is a Python decorator function that protects endpoints requiring authorization by checking the
    identity type and returning an error message if unauthorized.
    :return: The `admin_only` function returns a decorator function `wrapper`, which in turn returns a
    decorator function `decorator`. The `decorator` function checks if the user identity retrieved from
    `retrieve_jwt()` has a type of 1 (which presumably means an admin user), and if so, it calls the
    original function `fn` with the given arguments and returns its result. If the user identity
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
