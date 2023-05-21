from service import validator

@validator("User.name")
def username_validator(name):
    return True

@validator("User.dept")
def username_validator(dept):
    if dept >= 0:
        return True
    return False
