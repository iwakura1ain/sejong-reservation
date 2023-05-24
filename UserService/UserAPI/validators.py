from service import validator
from re import fullmatch

@validator("User.id")
def username_validator(id):
    return True

@validator("User.name")
def name_validator(name):
    return True

@validator("User.password")
def password_validator(password):
    return True if len(password) >= 8 else False

@validator("User.email")
def email_validator(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if fullmatch(regex, email) else False

@validator("User.dept")
def dept_validator(dept):
    return True if dept >= 0 else False

# TODO: optionize no_show
