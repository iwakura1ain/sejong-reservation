from service import validator, validate
from datetime import time

@validator("Room.is_usable")
def is_usable_validator(is_usable):
    """
    This is a validator function in Python that checks if a given input is an integer between 0 and 1.
    
    :param is_usable: The parameter "is_usable" is a variable that represents whether a room is usable
    or not. It is expected to be an integer value of either 0 or 1, where 0 means the room is not usable
    and 1 means the room is usable. The validator function checks if the
    :return: a boolean value (True or False) depending on whether the input value for "is_usable" is
    valid or not. If the input value is not an integer or is outside the range of 0 to 1, the function
    returns False. Otherwise, it returns True.
    """
    if (type(is_usable) != int
        or is_usable > 1
        or is_usable < 0):
        return False

    return True

@validator("Room.max_users")
def max_users_validator(max_users):
    """
    This is a validator function in Python that checks if the maximum number of users in a room is
    greater than zero.
    
    :param max_users: The parameter `max_users` is an integer representing the maximum number of users
    that can be in a room
    :return: If the `max_users` value is less than or equal to 0, the function returns `False`.
    Otherwise, it returns `True`.
    """
    if max_users <= 0:
        return False
    
    return True

# checks validity of open, close times for room
@validator("Room.open_time", "Room.close_time")
def validate_time(open_time, close_time):
    """
    This Python function validates the validity of open and close times for a room.
    
    :param open_time: The opening time of a room, represented as a string in ISO format (e.g.
    "09:00:00")
    :param close_time: The closing time of a room, represented as a string in ISO format (e.g.
    "18:00:00")
    :return: a boolean value. It returns True if the open_time is earlier than the close_time, and False
    otherwise. If there is an exception raised during the conversion of the input strings to time
    objects, the function returns False.
    """
    try:
        open_time = time.fromisoformat(open_time)
        close_time = time.fromisoformat(close_time)
    except Exception:
        return False

    return True if open_time < close_time else False



