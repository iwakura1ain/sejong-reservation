import base64

def serialization(data, include=[], exclude=[]):
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
    
