from flask import request
from flask_restx import Resource, namespace
from sqlalchemy import select, insert, update, delete
from service import Service, validate
from config import model_config, api_config
#import utils
from utils import serialization, check_jwt_exists

"""
This code creates a Flask-RestX namespace called "admin" with a name and description. Namespaces are
used to group related API endpoints together for easier organization and routing.
namespace for handy routing
"""
admin = namespace.Namespace(
    name="admin",
    description="유저, 회의실, 예약 관리를 위한 API"
)


# keys to be excluded when serializing data to GET all rooms
exclude = ['created_at', 'updated_at']

"""
The above code is defining a Flask RESTful API endpoint for managing conference rooms. It includes a
POST method for creating a new conference room and a GET method for retrieving all conference rooms.
The code also includes authorization checks to ensure that only authorized users can create or
retrieve conference rooms. The POST method validates the request body data and inserts the data into
the Room table in the database. The GET method retrieves all conference rooms from the Room table
and serializes the data before returning it as a response.
"""
@admin.route('/rooms')
class ConferenceRoom(Resource, Service):
    """
    This is the initialization function for a class that inherits from both Service and Resource
    classes, passing arguments to both parent classes.
    """
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    """
    This function creates a new room in a database table, Room, after validating the request body data and
    checking user authorization.

    :return: a JSON response with a message indicating whether the room was successfully created or
    not. If the user does not have authorization, the response will indicate that there is no
    authorization. If the room already exists in the database, the response will indicate that the
    room already exists. If there is an error during the creation of the room, the response will
    indicate that the room creation failed.
    """
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
                verified_json_body = Room.validate(req)
                res = conn.execute(select(Room)).mappings().all()
                
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
        
    """
    This function retrieves all rooms from the Room table and returns them as serialized data, along
    with a success message, or a failure message if there are no rooms or an error occurs.

    :return: This code returns a JSON response containing all the rooms in the Room table of the
    database, along with a success message. If there are no rooms in the table, it returns a message
    indicating that the room was not found. If there is an error, it returns a message indicating
    that the room GET failed.
    """
    # GET all rooms
    def get(self): 
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
        
"""
The above code defines a Flask route for handling GET, DELETE, and PATCH requests for a conference
room by its ID. It checks if the user is logged in and has authorization for DELETE and PATCH
requests. For GET request, it retrieves the conference room details by its ID from the database and
returns it in JSON format. For DELETE request, it deletes the conference room by its ID from the
database. For PATCH request, it updates the conference room details by its ID in the database. It
also validates the request body data before updating the conference room details.
GET, DELETE, UPDATE by room id
"""
@admin.route('/rooms/<int:id>')
class ConferenceRoomById(Resource, Service):
    """
    This is the initialization function for a class that inherits from both Service and Resource
    classes, passing arguments to both parent classes.
    """
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    # GET room by id    
    """
    This function retrieves a room by its ID and returns its details in a dictionary format.
    
    :param id: The id of the room that we want to retrieve

    :return: This code returns a JSON response containing the details of a room with the given id if
    it exists in the database. If the user is not logged in, it returns a message indicating that
    the user is not logged in. If the room with the given id does not exist in the database, it
    returns a message indicating that the room was not found. If there is an error while executing
    the code,
    """
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
                    }, 400
                
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
    """
    This function deletes a room by its ID after checking user authorization.    
    
    :param id: The id parameter is the unique identifier of the room that needs to be deleted

    :return: a dictionary with a "message" key indicating the status of the room deletion process. If
    the deletion is successful, the message will be "Room Deleted" with a status code of 200. If the
    room with the given id is not found, the message will be "Room id:{id} not found" with a status code
    of 400. If there is an error during
    """    
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
    """
    This is a Python function that updates a room in a database, with authorization and validation
    checks.
    
    :param id: The parameter "id" is the identifier of the room that needs to be updated. It is used
    to locate the specific room in the database and update its information
    
    :return: a JSON response with a message indicating whether the room update was successful or
    not. If the update was successful, the message will be "Room Updated" with a status code of 200.
    If the update failed, the message will be "Room Update Failed" with a status code of 500. If the
    user does not have authorization to update the room, the message will be
    """
    def patch(self, id):
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
                # validate request body data
                # SELECT room by id and parse it into dict
                verified_json_body = Room.validate(req)
                res = conn.execute(select(Room)).mappings()
                roomById = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no such room by given id
                if roomById is None:
                    return {
                        "message": f"Room id:{id} not found"
                    }, 400
                
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
                        # "room_name": verified_json_body['room_name'],
                        # "room_address1": verified_json_body['room_address1'],
                        # "room_address2": verified_json_body['room_address2'],
                        # "max_users": verified_json_body['max_users'],
                        # "is_usable": verified_json_body['is_usable'],
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
