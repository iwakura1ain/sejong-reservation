from flask import Flask, request
from flask_restx import Resource, namespace, Api
from sqlalchemy import select, insert, update, delete
from service import Service
import os

app = Flask(__name__)
api = Api(app)

# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass

# # admin = namespace.Namespace(
# #     name="admin",
# #     description="유저, 회의실, 예약 관리를 위한 API"
# )

model_config = {
    "username": "testusr",
    "password": "1234",
    "host": "db-service",
    "database": "exampledb",
    "port": 3306,
}

@api.route('/rooms')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)

    # GET Room
    def get(self): 
        roomName = request.json.get('roomName')    
        try:
            with self.query_model() as (conn, Room):
                res = conn.execute(select(Room).where(Room.roomName == roomName)).all()
                
                # if there's no such room
                if len(res) == 0:
                    return {
                        "message": "Room Not Found"
                    }, 200
                
                return res, {
                    "message": f"Room {roomName} Found"
                }, 200
                
        except Exception as e:
            print(e)
            return {
                "message": "Room Get Failed"
            }, 500    

    # CREATE Room
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
                "message": "Room Create Failed"
            }, 500
        
    # UPDATE Room
    def put(self):
        roomName = request.json.get('roomName')
        roomDesc = request.json.get('roomDecs')
        roomAddress1 = request.json.get('roomAddress1')
        roomAddress2 = request.json.get('roomAddress2')
        maxUsers = request.json.get('maxUsers')        
        try:
            with self.query_model() as (conn, Room):
                res = conn.execute(select(Room).where(Room.roomName == roomName)).all()
                
                # if there's no such room
                if len(res) == 0:
                    return {
                        "message": "Room Not Found"
                    }, 200
                
                conn.execute(
                    update(Room), {
                    "roomName": roomName,
                    "roomDesc": roomDesc,
                    "roomAdderss1": roomAddress1,
                    "roomAddress2": roomAddress2,
                    "maxUsers": maxUsers,
                    }
                )

                return {
                    "message": "Room Updated"
                }, 200

        except Exception as e:
            print(e)
            return {
                "message": "Room Update Failed"
            }, 500
        
    # DELETE Room
    def delete(self):
        roomName = request.json.get('roomName')
        try:
            with self.query_model() as (conn, Room):
                res = conn.execute(select(Room).where(Room.roomName == roomName)).all()

                if len(res) == 0:
                    return {
                        "message": "Room Not Found"
                    }, 200
                
                conn.execute(
                    delete(Room), {"roomName": roomName}
                )

                return {
                    "message": "Room Deleted"
                }, 200

        except Exception as e:
            print(e)
            return {
                "message": "Room Delete Failed"
            }, 500
        
# api.add_namespace(admin, '/rooms')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 