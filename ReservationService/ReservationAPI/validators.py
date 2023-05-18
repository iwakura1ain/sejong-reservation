from datetime import date, time
import json
import re

from service import validator


@validator("Reservation.start_time")
def validate_start_time(start_time):
    try:
        start_time = time.fromisoformat(start_time)
    except Exception as e:
        return False
    return True

@validator("Reservation.end_time")
def validate_end_time(end_time):
    try:
        end_time = time.fromisoformat(end_time)
    except Exception as e:
        return False
    return True

@validator("Reservation.start_time", "Reservation.end_time")
def validate_time(start_time, end_time):
    """
    checks validity of reservation's start_time and end_time 
    - start_time should be earlier than end_time.
    - reservation should be within open hours.
    """
    # check if time values are passed in with proper formattng
    print(type(start_time), end_time, flush=True)
    if start_time >= end_time:
        return False
    return True

@validator("Reservation.members")
def validate_members_list(members):
    """
    checks if members are in correct form
    """
    members = json.loads(members)
    for member in members:
        # check if only these keys exist
        if member.keys() != ["name", "email"]:
            return False
        # TODO: validate member name needed?
        # # validate member email with regex
        # pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # if not (re.match(pattern, member["email"])):
        #     return False
    return True

@validator("Reservation.reservation_topic")
def validate_reservation_topic(reservation_topic):
    """
    reservation_topic string len check
    """
    if len(reservation_topic) > 100:
        return False
    return True
