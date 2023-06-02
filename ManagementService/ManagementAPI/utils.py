from datetime import datetime, date, time

def serialize(data, include=[], exclude=[]):
    """
    The function serializes data by converting datetime, date, and time objects to strings.
    
    :param data: The data parameter is a dictionary containing the data that needs to be serialized
    :param include: The include parameter is a list of keys that should be included in the serialized
    data. If this parameter is not empty, only the keys in the list will be included in the output
    :param exclude: The `exclude` parameter is a list of keys that should be excluded from the
    serialized data. If a key in the `exclude` list is found in the `data` dictionary, it will not be
    included in the `serialized_data` dictionary that is returned
    :return: The function `serialize` takes in a dictionary `data` and two optional lists `include` and
    `exclude`. It serializes the data by converting any `datetime`, `date`, or `time` objects to strings
    and returns the serialized data as a dictionary.
    """
    row = dict(data)
    ret = {}
    for k, v in row.items():
        
        if type(v) in [datetime, date, time]:
            ret[k] = str(v)
        else:
            ret[k] = v
    return ret
    
def check_jwt_exists(auth_info):
    """
    The function checks if a JWT (JSON Web Token) exists in the given authentication information.
    
    :param auth_info: The auth_info parameter is a dictionary that contains information about the
    authentication status of a user. The function checks if the "status" key exists in the dictionary
    and returns its value. If the "status" key does not exist, the function returns False
    :return: a boolean value. If the "status" key is not present in the dictionary passed as an
    argument, it returns False. Otherwise, it returns the value associated with the "status" key.
    """
    if "status" not in auth_info.keys():
        return False
    return auth_info["status"]

from sqlalchemy import select

def check_if_room_identical(conn, Room, valid_data):
    """
    This function checks if a room in a database is identical to valid data based on its name and
    address.
    
    :param conn: The database connection object used to execute SQL queries
    :param Room: The Room parameter is likely a SQLAlchemy model class representing a table in a
    database. It is used to construct SQL queries to check if a room with certain attributes already
    exists in the database
    :param valid_data: It is a dictionary containing valid data for a room, including the room name,
    address line 1, and address line 2
    :return: a boolean value (True or False) depending on whether a room with the same name, address1,
    and address2 already exists in the database.
    """
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
    print("--------------------receivers:", receivers, flush=True)
    print("--------------------memebrs:", members_emails, flush=True)

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
