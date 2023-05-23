from service import validator

@validator("User.id")
def id_validator(id):
    return True

@validator("User.password")
def id_validator(password):
    return True

@validator("User.email")
def email_validator(email):
    return True

@validator("User.dept")
def dept_validator(dept):
    if dept >= 0:
        return True
    return False
