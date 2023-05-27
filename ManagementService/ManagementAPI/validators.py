from service import validator, validate

from datetime import time



@validator("Room.is_usable")
def is_usable_validator(is_usable):
    if (type(is_usable) != int
        or is_usable > 1
        or is_usable < 0):
        return False

    return True

@validator("Room.max_users")
def max_users_validator(max_users):
    if max_users <= 0:
        return False
    
    return True


@validator("Room.open_time", "Room.close_time")
def validate_time(open_time, close_time):
    """
    checks validity of open, close times for room
    """
    try:
        open_time = time.fromisoformat(open_time)
        close_time = time.fromisoformat(close_time)
    except Exception:
        return False

    return True if open_time < close_time else False



