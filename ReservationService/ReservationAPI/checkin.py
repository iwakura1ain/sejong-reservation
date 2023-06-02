from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, and_

import json
import hashlib

from datetime import date, time, datetime

from config import model_config, api_config, MINIMIZED_COLS
from service import Service

import json

from utils import (
    serialize,
    is_valid_token, is_admin, is_authorized,
    check_date_constraints,
    check_time_conflict,
    protected
)

CHECK_IN = Namespace(
    name="checkin",
    description="namespace for checking in",
    prefix="/check-in"
)

#REGISTERED_ROOMS = {}


@CHECK_IN.route("/<int:room_id>/register")
class RegisterCheckIn(Resource, Service):
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing arguments to their respective initialization functions.
        """
        Service.__init__(self, model_config=model_config,
                         api_config=api_config)
        Resource.__init__(self, *args, **kwargs)
        self.auth_info = None

    @protected()
    def get(self, room_id):
        """
        This is a protected function that registers a room and returns a room hash if the user is
        authorized.
        
        :param room_id: The ID of the room that needs to be registered
        :return: a dictionary with a "status" key and a "msg" key, along with an HTTP status code. The
        specific content of the "status" and "msg" keys depends on the outcome of the function's
        execution.
        """
        try:
            if not is_admin(self.auth_info):
                return {
                    "status": False,
                    "msg": "user not authorized"
                }, 400

            room = self.query_api(
                "get_rooms_info", "get",
                headers=request.headers,
                request_params={"id": room_id}
            )
            if room is None:
                return {
                    "status": False,
                    "msg": "no room found"
                }, 400

            room_hash = hashlib.sha256(str(room).encode('utf-8')).hexdigest()
            room_location_hash = hashlib.sha256(
                str(request.remote_addr + room_hash).encode("utf-8")
            ).hexdigest()

            res = self.query_api(
                "patch_rooms_info", "patch",
                headers=request.headers,
                request_params={"id": room_id},
                body=json.dumps({"location_hash": room_location_hash})
            )
            if res.get["status"]:
                return {
                    "status": True,
                    "msg": "room registered",
                    "room_hash": room_hash
                }, 200

        except Exception:
            return {
                "status": False,
                "msg": "room register failed"
            }, 200


@CHECK_IN.route("/<int:room_id>")
class CheckIn(Resource, Service):
    """
    The ReservationList class defines methods for getting a list of reservations and making a new
    reservation, with various filtering and validation checks.
    """

    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing arguments to their respective initialization functions.
        """
        Service.__init__(self, model_config=model_config,
                         api_config=api_config)
        Resource.__init__(self, *args, **kwargs)
        

    @staticmethod
    def get_current_reservation(conn, model, room_id):
        """
        This function retrieves the current reservation for a given room based on the current date and
        time.
        
        :param conn: The database connection object used to execute the SQL query
        :param model: The model parameter is likely a SQLAlchemy model class that represents a table in
        a database. It is used to construct a SQL query to retrieve a current reservation for a specific
        room
        :param room_id: The ID of the room for which we want to get the current reservation
        :return: The `get_current_reservation` method returns the current reservation for a given room
        at the current date and time. It queries the database using the provided `conn` connection
        object and the `model` SQLAlchemy model class. It filters the results to only include
        reservations that are active at the current time. The method returns the result as a mapping
        object or `None` if no reservation is found.
        """
        current = datetime.now()
        cur_date = current.date()
        cur_time = current.time().replace(microsecond=0)
        
        res = conn.execute(
            select(model)
            .where(model.room_id == room_id)
            .where(model.reservation_date == cur_date)
            .filter(and_(
                model.start_time <= cur_time,
                model.end_time >= cur_time,
            ))
        ).mappings().fetchone()

        return res

    @staticmethod
    def validate(data):
        """
        The function validates reservation code and room hash data and returns valid and invalid data in
        separate dictionaries.
        
        :param data: a dictionary containing the reservation code and room hash as keys and their
        respective values as values
        :return: The `validate` method is returning two dictionaries - `valid` and `invalid`. The
        `valid` dictionary contains the valid reservation code and room hash values, while the `invalid`
        dictionary contains the invalid reservation code and room hash values.
        """
        code = data.get("reservation_code")
        room_hash = data.get("room_hash")

        valid, invalid = {}, {}
        if type(code) == str and len(code) == 8:
            valid["reservation_code"] = code
        else:
            invalid["reservation_code"] = code

        if type(room_hash) == str:
            valid["room_hash"] = room_hash
        else:
            invalid["room_hash"] = room_hash
                
        return valid, invalid

    @staticmethod
    def get_location_hash(reservation_code, room_hash):
        """
        This is a static method in Python that generates a SHA256 hash based on a reservation code and a
        room hash concatenated with the IP address of the requester.
        
        :param reservation_code: The reservation code is a unique identifier for a specific reservation
        made by a customer. It is likely a string of characters or numbers that is generated when the
        reservation is created
        :param room_hash: The `room_hash` parameter is a unique identifier for a specific room. It is
        used to generate a hash that is unique to the combination of the user's IP address and the room
        identifier, which is then used as a location hash for the reservation
        """
        room_location_hash = hashlib.sha256(
            str(request.remote_addr + room_hash).encode("utf-8")
        ).hexdigest()
            

    # get reservation at current time
    def get(self, room_id):
        """
        This function retrieves the current reservation for a given room ID and returns it as a
        serialized object.
        
        :param room_id: The ID of the room for which the reservation is being retrieved
        :return: a dictionary with a "status" key indicating whether the operation was successful or
        not, a "msg" key with a message describing the result of the operation, and a "reservation" key
        with the details of the reservation if one was found. The HTTP status code is also included in
        the return statement.
        """
        with self.query_model("Reservation") as (conn, Reservation):
            try:
                room = self.query_api(
                    "get_rooms_info", "get",
                    headers=request.headers,
                    request_params={"id": room_id}
                )
                if "status" not in room.keys() or not room["status"]:
                    return {
                        "status": False,
                        "msg": "Invalid room ID"
                    }, 400
                
                res = self.get_current_reservation(conn, Reservation, room_id)
                
                if res is None:
                    return {
                        "status": False,
                        "msg": "no reseration for current time"
                    }, 400
                
                return {
                    "status": True,
                    "msg": "reservation for current time found",
                    "reservation": serialize(res)
                }, 200

            except Exception:
                return {
                    "status": False,
                    "msg": "error retrieving reservation for current time"
                }, 500
            
            
    # verify reservation_code(no_show code)
    def post(self, room_id):
        """
        This function verifies a reservation code and checks in the corresponding reservation for a
        given room.
        
        :param room_id: The ID of the room being reserved
        :return: This code returns a response in JSON format with a status and message indicating
        whether the reservation was successfully checked in or not. If there are any errors or invalid
        input, appropriate error messages are returned.
        """
        with self.query_model("Reservation") as (conn, Reservation):
            try:
                valid, invalid = self.validate(request.json)
                if len(invalid) != 0:
                    return {
                        "status": False,
                        "msg": "invalid key:val pairs",
                        "invalid": invalid
                    }, 400

                room = self.query_api(
                    "get_rooms_info", "get",
                    headers=request.headers,
                    request_params={"id": room_id}
                )
                if "status" not in room.keys() or not room["status"]:
                    return {
                        "status": False,
                        "msg": "Invalid room ID"
                    }, 400

                reservation = self.get_current_reservation(
                    conn, Reservation, room_id
                )
                if reservation is None:
                    return {
                        "status": False,
                        "msg": "no reservation for current time"
                    }, 400

                reservation_code = valid["reservation_code"]
                room_location_hash = self.get_location_hash(
                    valid["reservation_code"], valid["room_hash"]
                )

                if (reservation["reservation_code"] == reservation_code
                    and room["location_hash"] == room_location_hash):
                    conn.execute(
                        update(Reservation)
                        .where(Reservation.id == reservation["id"])
                        .values(room_used=1)
                    )
                    
                    return {
                        "status": True,
                        "msg": "reservation checked in",
                    }, 200

                return {
                    "status": False,
                    "msg": "reservation code wrong",
                }, 400

            except OSError:
                return {
                    "status": False,
                    "msg": "error retrieving reservation for current time"
                }, 500
        
