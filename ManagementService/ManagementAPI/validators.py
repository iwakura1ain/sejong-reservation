from service import validator, validate

@validator("Room.room_name")
def room_name_validator(room_name):

    if len(room_name) > 40:
        return False

    return True

@validator("Room.room_address1")
def room_address1_validator(room_address1):
    if len(room_address1) > 80:
        return False

    return True

@validator("Room.room_address2")
def room_address2_validator(room_address2):
    if len(room_address2) > 80:
        return False

    return True

@validator("Room.is_usable")
def is_usable_validator(is_usable):
    if (type(is_usable) != int
        or is_usable > 1
        or is_usable < 0):
        return False

    return True

@validator("Room.max_users")
def max_users_validator(max_users):
    if (type(max_users) != int
        and max_users <= 0):
        return False
    
    return True
