from datetime import date, time, datetime
import json
import re

from service import validator

@validator("Reservation.reservation_date")
def alwaysfalse(reservation_date):
    return False

@validator("Reservation.reservation_date")
def validate_end_time(reservation_date):
    try:
        reservation_date = time.fromisoformat(reservation_date)
    except ValueError:
        return False
    cur_date = datetime.now().date()

    return False if reservation_date < cur_date else True

@validator("Reservation.start_time")
def validate_start_time(start_time):
    try:
        start_time = time.fromisoformat(start_time)
    except ValueError:
        return False

    # check if start time is after time.now()
    cur_time = datetime.now().time()
    if start_time < cur_time:
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

        # # TODO: maybe use library for email verification
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
