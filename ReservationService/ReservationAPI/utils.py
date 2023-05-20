from sqlalchemy import select, func

import json
from datetime import date, time ,timedelta

def serialize(row):
    return json.loads(json.dumps(dict(row), default=str))

def is_valid_token(auth_info):
    """
    checks if token is valid.
    """
    if auth_info["msg"] == "Token has expired" \
        or auth_info["status"] == False:
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

def check_time_conflict(conn, Reservation, new_reservation):
    """
    checks time conflict by checking for date, room, 
    and start_time or end_time in between new_reservation
    """
    new_start_time = new_reservation["start_time"]
    new_end_time = new_reservation["end_time"]
    stmt = (select(Reservation.id, Reservation.reservation_date,
        Reservation.start_time, Reservation.end_time, Reservation.room_id)
        .where(Reservation.reservation_date == new_reservation["reservation_date"])
        .where(Reservation.room_id == new_reservation["room_id"])
        .filter(func.time(Reservation.start_time).between(new_start_time, new_end_time))
        .filter(func.time(Reservation.end_time).between(new_start_time, new_end_time)))
    rows = conn.execute(stmt).mappings().fetchall()
    return [serialize(row) for row in rows]

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
    diff = date.today() - date.fromisoformat(new_reservation["reservation_date"])
    if auth_info["User"]["type"] == 1 or auth_info["User"]["type"] == 2:
        pass
    elif auth_info["User"]["type"] == 3 and diff > timedelta(weeks=1):
        return "User(grad) cannot make reservation for this date"
    elif auth_info["User"]["type"] == 4 and diff > timedelta(days=2):
        return "User(undergrad) cannot make reservation for this date"
    return None


def create_confirmation_email(
    reservation, room, creator,
    sender="reservation_admin@sejong.ac.kr",
    title="[회의실 예약 시스템] 회의실 예약이 완료되었습니다",
    template_name="template-new-reservation.md"
):
    """
    Generates an alert email for when new reservation is created.
    sender: email address that sends out alert emails
    title: email title
    template_name: email body template file name

    Returns a dict for POST alertservice/alert body
    """

    members_emails = [member["email"] for member in reservation["members"]]
    receivers = [creator["email"]] + members_emails

    template_data = {
        "reservation_topic": reservation["reservation_topic"],
        "reservation_date": reservation["reservation_date"],
        "start_time": reservation["start_time"],
        "end_time": reservation["end_time"],
        "members_len": len(members_emails),
        "members_emails": ", ".join(members_emails),
        "code": reservation["reservation_code"],

        "room_name": room["room_name"],
        "room_address1": room["room_address1"],
        "room_address2": room["room_address2"],

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
