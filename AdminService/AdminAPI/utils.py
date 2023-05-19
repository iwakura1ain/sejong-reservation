def serialization(data, include=[], exclude=[]):
    serialized_data = {}
    
    if include:
        serialized_data = data.copy()
        for key in include:
            serialized_data[key] = None
    
    if exclude:
        serialized_data = dict((k, v) for k, v in data.items() if k not in exclude)

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
    
# import base64
# def check_preview_image(conn, Room, preview_image):
#     if preview_image:
#         if len(preview_image) % 4 != 0:
#             preview_image = preview_image.replace(" ", "")

#             padding_needed = len(preview_image) % 4
#             preview_image += "=" * (4 - padding_needed)

#             try:
#                 preview_image = base64.b64decode(preview_image)
#                 # 성공적으로 변환되었을 경우에 대한 추가 처리
#                 conn.execute(select(Room).where)
#             except Exception as e:
#                 # 변환 실패에 대한 예외 처리
#                 print("이미지 변환 실패:", str(e))
#         return preview_image

#     return False

# from sqlalchemy import insert, update
# def create_update_data(table, data, method):
#     if method == 'create':  
#         insert(table), {}
#         pass
#     elif method == 'update':
#         pass
#     else:
#         return "No Method"

