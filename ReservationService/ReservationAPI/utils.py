from sqlalchemy import select, and_

import re
import json
from datetime import datetime, date, time

from flask import request
from functools import wraps


def serialize(row):
    """
    The function serializes a row by converting it into a dictionary and then into a JSON object with
    string representation of non-serializable values.

    :param row: The parameter "row" is likely a dictionary or a row object from a database query result.

    :return: The function `serialize` is returning a dictionary that is created by converting the input
    `row` into a JSON string using `json.dumps`, and then converting that JSON string back into a
    dictionary using `json.loads`. The `default=str` argument is used to ensure that any
    non-serializable values in the `row` dictionary are converted to strings before being serialized.
    """
    row = dict(row)
    ret = {}
    for k, v in row.items():
        if k == "members":
            ret[k] = json.loads(v)
            
        elif type(v) in [datetime, date, time]:
            datetime_format = str(v).split(":")
            concat = lambda l: ":".join(l)
            ret[k] = concat(datetime_format[:-1]) if len(datetime_format) == 3 else concat(datetime_format)
            
        else:
            ret[k] = v
    return ret


def is_valid_token(response):
    """
    The function checks if a token is valid by verifying if the "status" key is present in the
    authentication information dictionary.

    :param auth_info: The auth_info parameter is a dictionary that contains information about an
    authentication token. 

    :return: a boolean value. If the "status" key is not present in the input dictionary "auth_info", it
    returns False. Otherwise, it returns the value associated with the "status" key, which is expected
    to be a boolean value indicating whether the token is valid or not.
    """
    if ("status" not in response.keys()
            or not response["status"]):
        return False
    return True


def is_authorized(auth_info, reservation):
    """
    check if user is authorized to change reservation
    - returns True if user is creator of reservation or admin
    - returns False otherwise
    """
    user = auth_info
    # user is creator of reservation
    if user["id"] == reservation["creator_id"]:
        return True
    # user is admin
    if user["type"] == 1:
        return True
    return False


def is_admin(auth_info):
    """
    The function checks if the user is an admin based on their authentication information.

    :param auth_info: It is a dictionary containing information about the user's authentication status.
    It includes information such as the user's ID, username, and the type of account (e.g. regular
    user or administrator).

    :return: a boolean value indicating whether the user is an admin or not. If the user is an admin,
    the function returns True, otherwise it returns False.
    """
    if auth_info["type"] == 1:
        return True
    return False


def check_time_conflict(reservation_dict, connection=None, model=None, reservation_id=None):
    """
    This function checks for time conflicts between a new reservation and existing reservations in a
    database.

    checks time conflict by checking for date, room, and start_time or end_time
    in between new_reservation
    
    - reservation_id is only used with PATCH
    returns true if confilts exist, else false.
    """
    reservation_date = reservation_dict["reservation_date"]
    room_id = reservation_dict["room_id"]
    new_start_time = reservation_dict["start_time"]
    new_end_time = reservation_dict["end_time"]

    rows = connection.execute(
        select(model)
        .where(model.reservation_date == reservation_date)
        .where(model.room_id == room_id)
        .filter(and_(
            model.start_time < new_end_time,
            model.end_time > new_start_time,
        ))
    ).mappings().fetchall()

    # if this function is called from PATCH
    if reservation_id:
        # if the only conflict is the reservation from PATCH, return false
        if len(rows) == 1 and rows[0].id == reservation_id:
            return False
        elif len(rows) == 0:
            return False
        return True

    # if this function is called from POST
    if len(rows) == 0:
        return False
    else:
        return True


def check_start_end_time(new_reservation, room):
    """
    This function checks the validity of a reservation's start and end times, ensuring they are within
    open hours and the start time is earlier than the end time.

    :param new_reservation: A dictionary containing information about a new reservation, including the
    start time and end time.

    :return: either a string indicating an error message if the reservation's start_time is later than
    the end_time or if the reservation is not within the open hours, or it returns None if the
    reservation's start_time and end_time are valid and within the open hours.
    """

    convert = lambda t: time.fromisoformat(t)
    
    reservation_start = convert(new_reservation["start_time"])
    reservation_end = convert(new_reservation["end_time"])

    print(room, flush=True)
    
    room_open = convert(room["open_time"])
    room_close = convert(room["close_time"])
    
    if room_open <= reservation_start and reservation_end <= room_close:
        return True
    return False

# check date constraints
def check_date_constraints(user_type, reservation_date):
    """
    This function checks if a user is authorized to make a reservation based on their user type and the
    reservation date constraints.
    
    :param user_type: The type of user making the reservation. It could be a regular user, a premium
    user, or an admin user
    :param reservation_date: The date for which the reservation is being made. It should be in the
    format of 'YYYY-MM-DD'
    :return: a boolean value. It returns True if the reservation date is within the date constraints for
    the user type, and False otherwise.
    """

    from config import reservation_limit

    diff = date.fromisoformat(reservation_date) - date.today()
    return True if diff <= reservation_limit[user_type] else False


def create_confirmation_email(
    reservation, room, creator, sender,
    title="[회의실 예약 시스템] 회의실 예약이 완료되었습니다. ",
    template_name="template.txt"
):
    """
    This function generates an email confirmation for a new reservation in a meeting room booking
    system.
    
    :param reservation: a dictionary containing information about the reservation, such as the
    reservation date, start and end times, members attending, and reservation code
    :param room: The room parameter is a dictionary containing information about the reserved room,
    including its name, address, and other details
    :param creator: A dictionary containing the name and email of the person who created the reservation
    :param sender: The email address that sends out the alert emails
    :param title: The title of the email that will be sent out as a confirmation for the reservation,
    defaults to [회의실 예약 시스템] 회의실 예약이 완료되었습니다.  (optional)
    :param template_name: The name of the file containing the email body template, defaults to
    template.txt (optional)
    :return: a dictionary with keys "title", "text", "sender", and "receivers". The values for these
    keys are generated based on the input parameters and the contents of a template file. The "title"
    key contains the email title, "text" contains the email body, "sender" contains the email address
    that sends out the alert emails, and "receivers" contains
    """
    """
    Generates an alert email for when new reservation is created.
    sender: email address that sends out alert emails
    title: email title
    template_name: email body template file name

    Returns a dict for POST alertservice/alert body
    """

    # set default text for missing info
    DEFAULT = "(내용없음)"

    # email title
    if "reservation_type" in reservation.keys():
        if reservation["reservation_type"] != None:
            title += "(정기예약)"
        else:
            title += "(단건예약)"

    # email receiver
    receivers = [creator["email"]]

    # reservation infos
    members_detail = DEFAULT
    if reservation["members"] != []:
        members = [f'{member["name"]} {member["email"]}' for member in reservation["members"]]
        members_detail = f"{1+len(members)}인 ({', '.join(members)})"
    reservation_topic = DEFAULT
    if reservation["reservation_topic"] != "":
        reservation_topic = reservation["reservation_topic"]

    template_data = {
        # reservation info
        "reservation_date": reservation["reservation_date"],
        "start_time": reservation["start_time"],
        "end_time": reservation["end_time"],
        "members_detail": members_detail,
        "reservation_topic": reservation_topic,
        "code": reservation["reservation_code"],
        # room info
        "room_name": room["room_name"],
        "room_address1": room["room_address1"],
        "room_address2": room["room_address2"],
        # creator info
        "creator": creator["name"],
        "creator_email": creator["email"],
    }

    with open(template_name, "r") as f:
        template = f.read()

    return {
        "title": title,
        "text": template.format(**template_data),
        "sender": sender,
        "receivers": receivers
    }

def validate_members(members):
    """
    The function validates a list of members by checking if each member has valid keys and a valid email
    address.
    
    :param members: The parameter "members" is expected to be a list of dictionaries, where each
    dictionary represents a member and contains two keys: "name" and "email". The function validates
    that each member dictionary has exactly these two keys and that the email value is a valid email
    address format. If any of these
    :return: a boolean value. It returns True if the input `members` is a list of dictionaries where
    each dictionary has keys "name" and "email", and the value of "email" is a valid email address. It
    returns False otherwise.
    """
    p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if type(members) != list:
        return False
    for member in members:
        # check each member for valid keys and valid email
        if list(member.keys()) != ["name", "email"]:
            return False
        if not p.match(member["email"]):
            return False
    return True

# decorator which protects endpoints that require authorization
def protected():
    """
    This is a Python decorator function that protects endpoints requiring authorization by checking for
    a valid token.
    :return: A decorator function named "protected" is being returned. This decorator function takes in
    another function as an argument and returns a new function that wraps the original function with
    additional functionality to protect endpoints that require authorization. The new function checks if
    the user has a valid token and sets the "auth_info" attribute of the object before calling the
    original function. If the user is not authenticated, it returns a JSON
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                _self = args[0]

                auth_info = _self.query_api(
                    "get_auth_info", "get", headers=request.headers
                )

                if not is_valid_token(auth_info):
                    return {
                        "status": False,
                        "msg": "Unauthenticated"
                    }, 400

                else:
                    _self.auth_info = auth_info["User"]

                return fn(*args, **kwargs)

            except OSError as e:
                print(e, flush=True)
                return {
                    "status": False,
                    "msg": "Reservation failed"
                }, 400

        return decorator
    return wrapper
