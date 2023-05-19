from sqlalchemy import select, func

import json
from datetime import date, time

def serialize(row):
    return json.loads(json.dumps(dict(row), default=str))

def is_valid_token(auth_info):
    """
    checks if token is valid.
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
    check if admin
    """
    # TODO 관리자가 아니더라도 user가 관리하는 방이면 관리자급 조회가능하도록?
    if auth_info["User"]["type"] == 1:
        return True
    return False

def check_time_conflict(reservation_dict, connection=None, model=None, reservation_id=False):
    """
    checks time conflict by checking for date, room, 
    and start_time or end_time in between new_reservation
    - reservation_id is only used with PATCH
    """
    reservation_date = reservation_dict["reservation_date"]
    room_id = reservation_dict["room_id"]
    new_start_time = reservation_dict["start_time"]
    new_end_time = reservation_dict["end_time"]

    stmt = (
        select(model)
        .where(model.reservation_date == reservation_date)
        .where(model.room_id == room_id)
        .filter(func.time(model.start_time).between(new_start_time, new_end_time))
        .filter(func.time(model.end_time).between(new_start_time, new_end_time))
    )
    
    # get all reservations from same date, same room with time conflict
    rows = connection.execute(stmt).mappings().fetchall()

    # check if this function is called in PATCH
    if reservation_id:
        # if the only conflict is the reservation from PATCH, return false
        if len(rows) == 1 and rows[0].id == reservation_id:
            return False
        return True

    # if this function is called from POST
    return True if len(rows) == 0 else False

def check_start_end_time(new_reservation):
    """
    checks validity of reservation's start_time and end_time 
    - start_time should be earlier than end_time.
    - reservation should be within open hours.
    """
    # check if start < end
    if new_reservation["start_time"] > new_reservation["end_time"]:
        return "End time earlier than start time"
    # check if start_time, end_time within open hours
    if time.fromisoformat(new_reservation["start_time"]) < time(9, 0) \
        or time.fromisoformat(new_reservation["end_time"]) > time(18, 0):
        return "Open hours: 0900~1800"
    return None

# check date constraints
def check_date_constraints(auth_info, new_reservation):
    """
    checks if user is allowed to make reservation for specified date.
    - returns None if allowed.
    - returns a message string if not allowed.
    """
    # diff = date.today() - date.fromisoformat(new_reservation["reservation_date"])
    # if auth_info["User"]["type"] == 1 or auth_info["User"]["type"] == 2:
    #     pass
    # elif auth_info["User"]["type"] == 3 and diff > timedelta(weeks=1):
    #     return "User(grad) cannot make reservation for this date"
    # elif auth_info["User"]["type"] == 4 and diff > timedelta(days=2):
    #     return "User(undergrad) cannot make reservation for this date"
    # return None

    # how far a user type can reserve ahead of time

    from config import reservation_limit
    
    user_type = auth_info["User"]["type"]
    reservation_date = new_reservation["reservation_date"]
    diff = date.fromisoformat(reservation_date) - date.today()
    return True if diff < reservation_limit[user_type] else False
    
        




