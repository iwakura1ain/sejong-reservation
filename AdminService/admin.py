from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, insert, update, delete
from service import Service

admin = namespace(
    name="admin",
    description="유저, 회의실, 예약 관리를 위한 API"
)

model_config = {
    "username": "testusr",
    "password": "1234",
    "host": "db-service",
    "database": "exampledb",
    "port": 3306,
}

# get room
@admin.route('/rooms')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)


    def post(self):
        roomName = request.json.get('roomName')
        roomDesc = request.json.get('roomDecs')
        roomAddress1 = request.json.get('roomAddress1')
        roomAddress2 = request.json.get('roomAddress2')
        maxUsers = request.json.get('maxUsers')
        try:
            with self.query_model() as (conn, Room):
                res = conn.execute(select(Room).where(Room.roomName == roomName)).all()

                if len(res) != 0:
                    return {
                        "message": "Room Exists"
                    }, 200
                
                conn.execute(
                    insert(Room), {
                    "roomName": roomName,
                    "roomDesc": roomDesc,
                    "roomAddress1": roomAddress1,
                    "roomAddress2": roomAddress2,
                    "maxUsers": maxUsers,
                    }
                )

                return{
                    "Message": "Room Created"
                }, 200
            
        except Exception as e:
            print(e)
            return {
                "message": "Room Creation Failed"
            }, 500

    # @admin.doc(response={200: 'Success'})
    # @admin.doc(response=(500: 'No Such Room'))
    def get(self):
        roomnumber = request.json.get('roomNumber')
        try:
            with self.query_model() as (conn, Room):
                res = conn.execute(select(Room).where(Room.roomnumber == roomnumber)).all()
                
                # if there's no such room
                if len(res) == 0:
                    return {
                        "message": "Room Not Found"
                    }, 200
                
        except Exception as e:
            print(e)
            return {
                "message": "Room GET Failed"
            }, 500