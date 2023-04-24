from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, update, delete
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
@admin.route('/get')
class ConferenceRoom(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)

    # @admin.doc(response={200: 'Success'})
    # @admin.doc(response=(500: 'No Such Room'))
    def get(self):
        roomnumber = request.json.get('roomNumber')
        try:
            with self.query_model() as (conn, Model):
                res = conn.execute(select(Model).where(Model.roomnumber == "roomnumber")).all()
                
                # if there's no such room
                # if len(res) == 0:
                #     return {
                #         "message": "Room Not Found"
                #     }, 200
                
                return res
                
        except Exception as e:
            print(e)
            return {
                "message": "Room Not Found"
            }, 500