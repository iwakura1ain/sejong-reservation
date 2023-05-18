from flask import request
from flask_restx import Resource, namespace

from sqlalchemy import select, insert, update, delete

from service import validator

from config import model_config, api_config

@validator("Room.room_name")
def room_name_validator(room_name):
    if len(room_name)>20:
        return False
    else:
        return True

@validator("Room.room_address1")
def room_address1_validator(room_adderss1):
    if len(room_adderss1)>20:
        return False
    else:
        return True

@validator("Room.room_address2")
def room_address2_validator(room_address2):
    if len(room_address2) > 20:
        return False
    else:
        return True

@validator("Room.is_usable")
def is_usable_validator(is_usable):
    if type(is_usable) != int:
        return False
    else:
        return True

@validator("Room.max_users")
def max_users_validator(max_users):
    if type(max_users) != int:
        return False
    
    if max_users <= 0:
        return False
    
    return True