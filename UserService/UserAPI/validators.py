from service import validator

# @validator("User.name")
# def name_validator(name):
#     return True

@validator("User.dept")
def dept_validator(dept):
    if dept >= 0:
        return True
    return False
