# import base64

def serialize(data, include=[], exclude=[]):
    serialized_data = {}
    
    if include:
        serialized_data = data.copy()
        for key in include:
            serialized_data[key] = None
    
    if exclude:
        serialized_data = dict((k, v) for k, v in data.items() if k not in exclude)

    # for key, value in serialized_data.items():
    #     if isinstance(value, bytes):
    #         serialized_data[key] = base64.b64encode(value).decode('utf-8')

    return serialized_data
    
def check_jwt_exists(auth_info):
    if "status" not in auth_info.keys():
        return False
    return auth_info["status"]

from sqlalchemy import select

def check_if_room_identical(conn, Room, valid_data):
    if (conn.execute(select(Room).where(Room.room_name == valid_data['room_name'])).mappings().fetchone()
        and conn.execute(select(Room).where(Room.room_address1 == valid_data['room_address1'])).mappings().fetchone()
        and conn.execute(select(Room).where(Room.room_address2 == valid_data['room_address2'])).mappings().fetchone()):
        return True
    
import json

def create_confirmation_email(
    reservation, room, creator,
    # sender="reservationsys_admin@sejong.ac.kr",
    sender="",
    title="[회의실 예약 시스템] 회의실 예약이 취소되었습니다",
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
    members_json = json.loads(reservation["members"])
    members_emails = [member["email"] for member in members_json]
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