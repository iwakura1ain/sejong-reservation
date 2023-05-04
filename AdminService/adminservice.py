from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, insert, update, delete
from service import Service, validate
import utils

# namespace for handy routing
admin = namespace.Namespace(
    name="admin",
    description="유저, 회의실, 예약 관리를 위한 API"
)

# model configuration for orm model
model_config = {
    "username": "testusr",
    "password": "1234",
    "host": "127.0.0.1",
    "database": "exampledb",
    "port": 3306,
}

# keys to be excluded when serializing data to GET all rooms
exclude = ['createdAt', 'updatedAt']

@admin.route('/rooms')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)

    # CREATE Room 
    def post(self):
        # request body data, need to be validated
        req = request.json
        try:
            with self.query_model("Room") as (conn, Room):
                # validate data from request body
                verified_json_body = Room.validate(req)
                res = conn.execute(select(Room)).mappings().all()
                
                # if validated data is already in table, 
                # send message 'data already exists'
                for room in res:
                    if verified_json_body['roomName'] in room['roomName']:
                        if verified_json_body['roomAddress1'] in room['roomAddress1']:
                            if verified_json_body['roomAddress2'] in room['roomAddress2']:
                                return{
                                    "message": f"Room {verified_json_body['roomName']} already exists." 
                                }, 200
                
                # insert verified body data to Room table
                conn.execute( 
                    insert(Room), {
                        "roomName": verified_json_body['roomName'],
                        "roomAddress1": verified_json_body['roomAddress1'],
                        "roomAddress2": verified_json_body['roomAddress2'],
                        "maxUsers": verified_json_body['maxUsers'],
                        "isUsable": verified_json_body['isUsable'],
                    }
                )

                # CREATE room
                return{
                    "Message": "Room Created"
                }, 200
        
        # error
        except Exception as e:
            print(e)
            return {
                "message": "Room Create Failed"
            }, 500
        
    # GET all rooms
    @admin.doc(responses={200: 'Success'})
    @admin.doc(responses={404: 'Fail'})
    def get(self): 
        try:
            with self.query_model("Room") as (conn, Room):
                # get all json data from Room table as list with dicts
                rooms = conn.execute(select(Room)).mappings().all()

                # serialize each room data in Room table
                serialized_rooms = []
                for room in rooms:
                    serialized_room = utils.serialization(room, exclude=exclude)
                    serialized_rooms.append(serialized_room)

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
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)
    
    # GET room by id
    def get(self, id):
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 400
                
                # GET room with given id
                return {
                    "id": res.id,
                    "roomName": res.roomName,
                    "roomAdderss1": res.roomAddress1,
                    "roomAddress2": res.roomAddress2,
                    "maxUsers": res.maxUsers,
                }, 200

        # error      
        except Exception as e:
            print(e)
            return {
                "message": "Room GET failed"
            }, 500
        
    # DELETE room by id
    def delete(self, id):
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 400
                
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
    def put(self, id):
        # request body data, need to be validated
        req = request.json
        try:
            with self.query_model("Room") as (conn, Room):
                # validate request body data
                # SELECT room by id and parse it into dict
                verified_json_body = Room.validate(req)
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no such room by given id
                if res is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 400
                
                # UPDATE room
                conn.execute(
                    update(Room).where(Room.id == id),{
                        "roomName": verified_json_body['roomName'],
                        "roomAddress1": verified_json_body['roomAddress1'],
                        "roomAddress2": verified_json_body['roomAddress2'],
                        "maxUsers": verified_json_body['maxUsers'],
                        "isUsable": verified_json_body['isUsable'],
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