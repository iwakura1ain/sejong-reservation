from sqlalchemy import select, and_

import re
import json
from datetime import datetime, date, time


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
            ret[k] = str(v)
        else:
            ret[k] = v
    return ret


def is_valid_token(auth_info):
    """
    The function checks if a token is valid by verifying if the "status" key is present in the
    authentication information dictionary.

    :param auth_info: The auth_info parameter is a dictionary that contains information about an
    authentication token. 

    :return: a boolean value. If the "status" key is not present in the input dictionary "auth_info", it
    returns False. Otherwise, it returns the value associated with the "status" key, which is expected
    to be a boolean value indicating whether the token is valid or not.
    """
    if ("status" not in auth_info.keys()
            or not auth_info["status"]):
        return False
    return True


def is_authorized(auth_info, reservation):
    """
    check if user is authorized to change reservation
    - returns True if user is creator of reservation or admin
    - returns False otherwise
    """
    user = auth_info["User"]
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
    if auth_info["User"]["type"] == 1:
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

    stmt = (select(model)
        .where(model.reservation_date == reservation_date)
        .where(model.room_id == room_id)
        .filter(and_(
            model.start_time < new_end_time,
            model.end_time > new_start_time,
        ))
    )

    rows = connection.execute(stmt).mappings().fetchall()
    print(rows, flush=True)

    # check if this function is called in PATCH
    # TODO: check for PATCH
    if reservation_id:
        # if the only conflict is the reservation from PATCH, return false
        if len(rows) == 1 and rows[0].id == reservation_id:
            return False
        return True

    # if this function is called from POST
    if len(rows) == 0:
        return False
    else:
        return True


def check_start_end_time(new_reservation):
    """
    This function checks the validity of a reservation's start and end times, ensuring they are within
    open hours and the start time is earlier than the end time.

    :param new_reservation: A dictionary containing information about a new reservation, including the
    start time and end time.

    :return: either a string indicating an error message if the reservation's start_time is later than
    the end_time or if the reservation is not within the open hours, or it returns None if the
    reservation's start_time and end_time are valid and within the open hours.
    """
    # check if start < end
    if new_reservation["start_time"] > new_reservation["end_time"]:
        return "End time earlier than start time"
    # check if start_time, end_time within open hours
    if (time.fromisoformat(new_reservation["start_time"]) < time(9, 0)
        or time.fromisoformat(new_reservation["end_time"]) > time(18, 0)):
        return "Open hours: 0900~1800"
    return None

# check date constraints
def check_date_constraints(user_type, reservation_date):
    """
    This function checks if a user is authorized to make a reservation based on their user type and the
    reservation date constraints.


    :return: False if the date constraints are not met based on the user type, otherwise it
    returns True.
    """

    from config import reservation_limit

    diff = date.fromisoformat(reservation_date) - date.today()
    return True if diff < reservation_limit[user_type] else False


def create_confirmation_email(
    reservation, room, creator,
    # sender="reservationsys_admin@sejong.ac.kr",
    sender="",
    title="[회의실 예약 시스템] 회의실 예약이 완료되었습니다",
    template_name="template.txt"
):
    """
    Generates an alert email for when new reservation is created.
    sender: email address that sends out alert emails
    title: email title
    template_name: email body template file name

    Returns a dict for POST alertservice/alert body
    """
    # TODO: refactor to account for cases when some info are missing

    members_emails = [member["email"] for member in reservation["members"]]
    receivers = [creator["email"]]

    template_data = {
        # reservation info
        "reservation_date": reservation["reservation_date"],
        "start_time": reservation["start_time"],
        "end_time": reservation["end_time"],
        "members_len": len(members_emails),
        "members_emails": ", ".join(members_emails),
        "code": reservation["reservation_code"],
        "reservation_topic": reservation["reservation_topic"],
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

def 
