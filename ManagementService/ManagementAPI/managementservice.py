from flask import request, send_from_directory
from flask_restx import Resource, namespace

from sqlalchemy import select, insert, update, delete

from werkzeug.utils import secure_filename
import os
import json

from service import Service

from config import (
    model_config, 
    api_config, 
    filepath,
    SENDER
)
from utils import (
    serialize, 
    check_jwt_exists, 
    check_if_room_identical,
    create_confirmation_email
)

"""
This code creates a Flask-RestX namespace called "management" with a name and description. Namespaces are
used to group related API endpoints together for easier organization and routing.
namespace for handy routing
"""

management = namespace.Namespace(
    name="management",
    description="회의실 관리를 위한 API"
)

# keys to be excluded when serializing data to GET all rooms
exclude = ['created_at', 'reservation_date', 'open_time', 'close_time']

@management.route('/rooms')
class ConferenceRoom(Resource, Service):
    """
    The above code is defining a Flask RESTful API endpoint for managing conference rooms. It includes a
    POST method for creating a new conference room and a GET method for retrieving all conference rooms.

    The code also includes authorization checks to ensure that only authorized users can create or
    retrieve conference rooms.

    The POST method validates the request body data and inserts the data into
    the Room table in the database.

    The GET method retrieves all conference rooms from the Room table
    and serializes the data before returning it as a response.
    """
    
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing arguments to both parent classes.
        """
        
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    # CREATE room 
    def post(self):
        """
        This function creates a new room in a database table, Room, after validating the request body data and
        checking user authorization.

        :return: a JSON response with a message indicating whether the room was successfully created or
        not. If the user does not have authorization, the response will indicate that there is no
        authorization. If the room already exists in the database, the response will indicate that the
        room already exists. If there is an error during the creation of the room, the response will
        indicate that the room creation failed.
        """
        
        # check user if has authorization.
        auth_info = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )

        if(check_jwt_exists(auth_info) 
           and (auth_info['User']['type'] != 1)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200

        try:
            with self.query_model("Room") as (conn, Room):
                valid_data, invalid_data = Room.validate(request.json, optional=True)
                if len(invalid_data) > 0:
                    return {
                        "status": False,
                        "msg": "invalid data",
                        "invalid": invalid_data
                    }, 200
                
                # if validated data is already in table, 
                # send message 'data already exists'
                if check_if_room_identical(conn, Room, valid_data):
                    return {
                        "status": False,
                        "msg": "Room already exists"
                    }, 200
                
                # insert verified body data to Room table
                conn.execute(
                    insert(Room), {
                        **valid_data
                    }
                )
                room = conn.execute(select(Room).where(Room.room_name == request.json['room_name'] 
                                                                and Room.room_address1 == request.json['room_address1']
                                                                and Room.room_address2 == request.json['room_address2'])
                                                                ).mappings().fetchone()
                
                room = serialize(room, exclude=exclude)
                del room['location_hash']
                del room['preview_image_name']

                # CREATE room
                return{
                    "status": True,
                    "msg": "Room created",
                    "created_room": room
                }, 200
        
        # error
        except Exception as e:
            return {
                "status": False,
                "msg": "Room CREATE failed"
            }, 500
        
    # GET all rooms
    def get(self): 
        """
        This function retrieves all rooms from the Room table and returns them as serialized data, along
        with a success message, or a failure message if there are no rooms or an error occurs.

        :return: This code returns a JSON response containing all the rooms in the Room table of the
        database, along with a success message. If there are no rooms in the table, it returns a message
        indicating that the room was not found. If there is an error, it returns a message indicating
        that the room GET failed.
        """
        try:
            with self.query_model("Room") as (conn, Room):
                # get all json data from Room table as list with dicts
                rooms = conn.execute(select(Room)).mappings().all()
            
                # serialize each room data in Room table
                serialized_rooms = [
                    serialize(room, exclude=exclude)
                    for room in rooms
                ]

                # if there's no such room
                if len(serialized_rooms) == 0:
                    return {
                        "status": True,
                        "msg": "No room exists",
                        "rooms": rooms
                    }, 200

                # GET all rooms
                return {
                    "status": True,
                    "allRooms": serialized_rooms,
                    "msg": "Room found"
                }, 200

        # error
        except Exception as e:
            return {
                "status": False,
                "msg": "Failed to get room data"
            }, 500
                
# GET, DELETE, UPDATE by room id
@management.route('/rooms/<int:id>')
class ConferenceRoomById(Resource, Service):
    """
    The above code defines a Flask route for handling GET, DELETE, and PATCH requests for a conference
    room by its ID. It checks if the user is logged in and has authorization for DELETE and PATCH
    requests. For GET request, it retrieves the conference room details by its ID from the database and
    returns it in JSON format. For DELETE request, it deletes the conference room by its ID from the
    database. For PATCH request, it updates the conference room details by its ID in the database. It
    also validates the request body data before updating the conference room details.
    GET, DELETE, UPDATE by room id
    """
    
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing arguments to both parent classes.
        """
        
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    # GET room by id    
    def get(self, id):
        """
        This function retrieves a room by its ID and returns its details in a dictionary format.
        
        :param id: The id of the room that we want to retrieve.

        :return: This code returns a JSON response containing the details of a room with the given id if
        it exists in the database. If the user is not logged in, it returns a message indicating that
        the user is not logged in. If the room with the given id does not exist in the database, it
        returns a message indicating that the room was not found. If there is an error while executing
        the code,
        """

        # # check if user is logged in.
        # auth_info = self.query_api( 
        #     "jwt_status", "get", headers=request.headers
        # )
        # if not check_jwt_exists(auth_info):
        #     return {
        #         "status": False,
        #         "msg": "Not logged in"
        #     }, 200

        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "status": False,
                        "msg": f"Room id:{id} not found"
                    }, 200
                
                serialized_room = serialize(res, exclude=exclude)
                
                # GET room with given id
                return {
                    "status": True,
                    "room": serialized_room,
                    "msg": f"Room id:{id} found",
                }, 200

        # error      
        except Exception as e:
            return {
                "status": False,
                "msg": "Room GET failed"
            }, 500
        
    # DELETE room by id
    def delete(self, id):
        """
        This function deletes a room by its ID after checking user authorization.    
        
        :param id: The id parameter is the unique identifier of the room that needs to be deleted.

        :return: a dictionary with a "message" key indicating the status of the room deletion process. If
        the deletion is successful, the message will be "Room Deleted" with a status code of 200. If the
        room with the given id is not found, the message will be "Room id:{id} not found" with a status code
        of 400. If there is an error during
        """
        
        # check user if has authorization.
        auth_info = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if(check_jwt_exists(auth_info) 
           and (auth_info['User']['type'] != 1)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # SELECT room by id and parse it into dict
                res = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()

                # if there's no room by given id
                if res is None:
                    return {
                        "status": True,
                        "msg": f"Room id:{id} not found"
                    }, 200
                
                # DELETE room
                conn.execute(
                    delete(Room).where(Room.id == id)
                )

                # DELETE room done
                return {
                    "status": True,
                    "msg": "Room Deleted"
                }, 200

        # error
        except Exception as e:
            return {
                "status": False,
                "msg": "Room Delete Failed"
            }, 500
        
    # UPDATE Room by id
    def patch(self, id):
        """
        This is a Python function that updates a room in a database, with authorization and validation
        checks.
        
        :param id: The parameter "id" is the identifier of the room that needs to be updated. It is used
        to locate the specific room in the database and update its information.
        
        :return: a JSON response with a message indicating whether the room update was successful or
        not. If the update was successful, the message will be "Room Updated" with a status code of 200.
        If the update failed, the message will be "Room Update Failed" with a status code of 500. If the
        user does not have authorization to update the room, the message will be
        """
        
        # check user if has authorization.
        auth_info = self.query_api(
            "jwt_status", "get", headers=request.headers
        )
        
        if (check_jwt_exists(auth_info)
           and (auth_info['User']['type'] != 1)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200
        
        try:
            with self.query_model("Room") as (conn, Room):
                # validate data i  request body
                valid_data, invalid_data = Room.validate(request.json, optional=True)

                # check if there's an invalid data in request body
                if len(invalid_data) > 0:
                    return {
                        "status": False,
                        "msg": "invalid data",
                        "invalid": invalid_data
                    }, 200

                roomById = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()
                # if there's no such room by given id
                if roomById is None:
                    return {
                        "status": False,
                        "msg": f"Room id:{id} not found"
                    }, 200

                # if updated room data already exists in the table
                if ('room_name' in valid_data
                    and 'room_address1' in valid_data
                    and 'room_address2' in valid_data):
                    # for room in valid_data:
                    if check_if_room_identical(conn, Room, valid_data):
                        return{
                            "statsus": False,
                            "msg": f"Room {valid_data['room_name']} already exists." 
                        }, 200

                # if room is not usable, cancel reservations of the room                   
                if (roomById['is_usable'] != 0
                    and valid_data['is_usable'] == 0):
                    with self.query_model("Reservation") as (conn, Reservation):
                        rsrvs = conn.execute(select(Reservation).where(Reservation.room_id == id)).mappings().fetchall()

                        for _ in rsrvs:
                            rsrv = conn.execute(select(Reservation.is_valid == 1))
                            conn.execute(
                                update(Reservation).where(Reservation.is_valid == 1),{
                                   "is_valid": 0
                                }
                            )

                        for rsrv in rsrvs:
                            email_object = create_confirmation_email(
                                rsrv, 
                                roomById, 
                                auth_info["User"], 
                                sender=SENDER)
                            email_resp = self.query_api(
                                "send_email", "post",
                                headers=request.headers, body=json.dumps(email_object)
                            )
                    
                # UPDATE room
                conn.execute(
                    update(Room).where(Room.id == id),{
                        **valid_data
                    }
                )

                # UPDATE room done
                return {
                    "status": True,
                    "msg": "Room Updated"
                }, 200

        # error
        except Exception as e:
            return {
                "status": False,
                "msg": "Room Update Failed"
            }, 500

@management.route('/rooms/<int:id>/image')
class ConferenceRoomImage(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def check_if_file_unique(joined_path):
        if os.path.exists(joined_path):
            return False
        return True

    def get(self, id):
        try:
            with self.query_model("Room") as (conn, Room):
                room = conn.execute(select(Room).where(Room.id == id)).mappings().fetchone()
                if len(room) == 0:
                    return {
                        "status": False,
                        "msg": "Room not found"
                    }, 200
                
                return send_from_directory(
                    filepath, room["preview_image_name"]
                )
            
        except Exception as e:
            return {
                "status": False,
                "msg": "Download image failed"
            }, 500
    
    # insert preview_image into a room found by id
    def post(self, id):
        max_file_size = 16 * 1000 * 1000 # file size set maximum 16MB
        uploaded_image = request.files['image']
    
        filename = secure_filename(uploaded_image.filename)
        joined_path = os.path.join(filepath, filename)
        
        # check user if has authorization.
        auth_info = self.query_api( 
            "jwt_status", "get", headers=request.headers
        )
        if(check_jwt_exists(auth_info) 
           and (auth_info['User']['type'] != 1)):
            return {
                "status": False,
                "msg": "No authorization"
            }, 200

        # error checking : does file exists
        if filename == '':
            return {
                "status": False,
                "msg": "No selected file"
            }, 200
        
        # error checking : is file in allowed extensions
        if not self.allowed_file(filename):
            return {
                "status": False,
                "msg": "Invalid file extension",
                "filename": filename
            }

        # error checking: is file unique
        if not self.check_if_file_unique(joined_path):
            return {
                "status": False,
                "msg": "File already exists"
            }, 200

        # check file size
        if ('Content-Length' in request.headers 
            and int(request.headers['Content-Length']) > max_file_size):
            return {
                "status": False,
                "msg": f"File size exceeds the maximum limit of {max_file_size}bytes"
            }, 200

        try:
            with self.query_model("Room") as (conn, Room):
                # insert file path into the data
                conn.execute(
                    update(Room).where(Room.id == id), {
                        "preview_image_name": filename
                    }
                )

                # save image
                uploaded_image.save(joined_path)

                # insert image
                return {
                    "status": True,
                    "msg": "Image uploaded",
                    # "uploaded": filename,
                    # "uploadedPath": joined_path
                }
        except Exception as e:
            return {
                "status": False,
                "msg": "Uploading image failed"
            }, 500

        
