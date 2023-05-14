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
            if identity["type"] == 2 or identity["id"] == int(kwargs["id"]):
                return fn(*args, **kwargs)
            
            return {
                "status": False,
                "msg": "unauthorized"
            }, 200
            
        return decorator
    return wrapper

@jwt_required_original
def jwt_required():
