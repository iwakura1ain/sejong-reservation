from service import validator
from re import fullmatch

@validator("User.id")
def id_validator(id):
    """
    The function "id_validator" returns True without performing any validation on the input parameter
    "id".
    
    :param id: The parameter "id" is a variable that represents an identification number or code. The
    function "id_validator" takes this parameter as input and returns a boolean value of True. However,
    this function does not actually validate the identification number in any way, so it may need to be
    modified to perform the
    :return: True.
    """
    return True

@validator("User.password")
def id_validator(password):
    """
    This is a placeholder function that always returns True and does not perform any validation on the
    password field of a User object.
    
    :param password: The parameter "password" is a string representing the password entered by the user
    :return: a boolean value of `True`.
    """
    return True

@validator("User.email")
def email_validator(email):
    """
    This is a placeholder email validator function that always returns True.
    
    :param email: The email parameter is a string representing an email address that is being validated
    :return: a boolean value of True.
    """
    return True

@validator("User.name")
def name_validator(name):
    """
    This is a placeholder function that always returns True and validates the "name" field of a user
    object.
    
    :param name: The parameter "name" is a string representing the name of a user. The validator
    function is designed to validate the format of the name and return a boolean value indicating
    whether the name is valid or not. However, the current implementation of the function simply returns
    True for any input, which means it does
    :return: The function `name_validator` is returning a boolean value `True`.
    """
    return True

@validator("User.password")
def password_validator(password):
    """
    This is a password validator function in Python that checks if the length of the password is at
    least 8 characters.
    
    :param password: The parameter "password" is a string representing the password entered by a user
    :return: a boolean value. It will return True if the length of the password is greater than or equal
    to 8, and False otherwise.
    """
    return True if len(password) >= 8 else False

@validator("User.email")
def email_validator(email):
    """
    This is a Python function that validates whether an email address is in the correct format using
    regular expressions.
    
    :param email: The email parameter is a string representing an email address that needs to be
    validated. The email_validator function uses a regular expression to check if the email address is
    valid or not. If the email address matches the regular expression, the function returns True,
    otherwise it returns False
    :return: a boolean value (True or False) based on whether the input email string matches the regular
    expression pattern defined in the regex variable.
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if fullmatch(regex, email) else False

@validator("User.dept")
def dept_validator(dept):
    """
    This is a validator function in Python that checks if the department value of a user is greater than
    or equal to zero.
    
    :param dept: The "dept" parameter is a field in the "User" model that represents the department of
    the user. The validator function is checking if the department value is greater than or equal to 0,
    and returning True if it is, and False otherwise. This validator function ensures that the
    department value is
    :return: a boolean value. It returns True if the value of "dept" is greater than or equal to 0, and
    False otherwise.
    """
    return True if dept >= 0 else False

# TODO: optionize no_show
