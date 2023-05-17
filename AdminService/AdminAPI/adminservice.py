from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, insert, update, delete
from service import Service, validate
from config import model_config, api_config
#import utils
from utils import serialization, check_jwt_exists

# namespace for handy routing
admin = namespace.Namespace(
    name="admin",
    description="유저, 회의실, 예약 관리를 위한 API"
)


# keys to be excluded when serializing data to GET all rooms
exclude = ['created_at', 'updated_at']

@admin.route('/rooms')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    # CREATE Room 
    def post(self):
        # request body data, need to be validated
        req = request.json

        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if(check_jwt_exists(user_status) 
           and user_status['User']['type'] != 2):
            return {
                "status": False,
                "message": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # validate data from request body
                verified_json_body, status = Room.validate(req)
                if status:
                    res = conn.execute(select(Room)).mappings().all()
                else:
                    return {
                        "msg": "validation fail",
                        "data": verified_json_body
                    }, 200
                
                # if validated data is already in table, 
                # send message 'data already exists'
                for room in res:
                    if (verified_json_body['room_name'] in room['room_name'] and 
                    verified_json_body['room_address1'] in room['room_address1'] and 
                    verified_json_body['room_address2'] in room['room_address2']):
                        return{
                            "message": f"Room {verified_json_body['room_name']} already exists." 
                        }, 200
                
                # insert verified body data to Room table
                conn.execute( 
                    insert(Room), {
                        "room_name": verified_json_body['room_name'],
                        "room_address1": verified_json_body['room_address1'],
                        "room_address2": verified_json_body['room_address2'],
                        "max_users": verified_json_body['max_users'],
                        "is_usable": verified_json_body['is_usable'],
                    }
                )

                # CREATE room
                return{
                    "Message": "Room Created"
                }, 200
        
        # error
        except OSError as e: # 모든 exception을 e로 받겠다, 그런데 지금 어디서 error가 나는지 모른다, 모든 exception을 받는게 아니라 특정한걸 받아보자
            print(e)
            return {
                "message": "Room Create Failed"
            }, 500
        
    # GET all rooms
    def get(self):     
        # check if user is logged in.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if not check_jwt_exists(user_status):
            return {
                "status": False,
                "message": "Not logged in",
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # get all json data from Room table as list with dicts
                rooms = conn.execute(select(Room)).mappings().all()
            
                # serialize each room data in Room table
                serialized_rooms = [
                    serialization(room, exclude=exclude)
                    for room in rooms
                ]

                # if there's no such room
                if len(serialized_rooms) == 0:
                    return {
                        "message": "Room Not Found"
                    }, 200

                # GET all rooms
                return {
                    "allRooms": serialized_rooms,
                    "message": "Room found"
                }, 200

        # error
        except Exception as e:
            print(e)
            return {
                "message": "Room Get Failed"
            }, 500
        
# GET, DELETE, UPDATE by room id
@admin.route('/rooms/<int:id>')
class ConferenceRoomById(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)
    
    # GET room by id    
    def get(self, id):
        # check if user is logged in.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if not check_jwt_exists(user_status):
            return {
                "status": False,
                "message": "Not logged in"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 200
                
                # GET room with given id
                return {
                    "id": res.id,
                    "room_name": res.room_name,
                    "roomAdderss1": res.room_address1,
                    "room_address2": res.room_address2,
                    "max_user's": res.max_users,
                }, 200

        # error      
        except Exception as e:
            print(e)
            return {
                "message": "Room GET failed"
            }, 500
        
    # DELETE room by id
    def delete(self, id):
        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if(check_jwt_exists(user_status) 
           and user_status['User']['type'] != 2):
            return {
                "status": False,
                "message": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 200
                
                # DELETE room
                conn.execute(
                    delete(Room).where(Room.id == id)
                )

                # DELETE room done
                return {
                    "message": "Room Deleted"
                }, 200

        # error
        except Exception as e:
            print(e)
            return {
                "message": "Room Delete Failed"
            }, 500
        
    # UPDATE Room
    def patch(self, id):
        # request body data, needs to be validated
        req = request.json
        
        # check user if has authorization.
        user_status = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if(check_jwt_exists(user_status)
           and user_status['User']['type'] != 2):
            return {
                "status": False,
                "message": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # validate data from request body
                verified_json_body, status = Room.validate(req)
                if status:
                    # SELECT room by id and parse it into dict
                    res = conn.execute(select(Room)).mappings().all()
                    roomById = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()
                else:
                    return {
                        "msg": "validation fail",
                        "data": verified_json_body
                    }, 200

                # if there's no such room by given id
                if roomById is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 200
                
                # if updated room data already exists in the table
                for room in res:
                    if (verified_json_body['room_name'] in room['room_name'] and 
                        verified_json_body['room_address1'] in room['room_address1'] and 
                        verified_json_body['room_address2'] in room['room_address2']):
                        return{
                            "message": f"Room {verified_json_body['room_name']} already exists." 
                        }, 200

                
                # UPDATE room
                conn.execute(
                    update(Room).where(Room.id == id),{
                        **verified_json_body 
                    }
                )

                # UPDATE room done
                return {
                    "message": "Room Updated"
                }, 200

        # error
        except Exception as e:
            print(e)
            return {
                "message": "Room Update Failed"
            }, 500
