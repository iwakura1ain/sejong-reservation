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
                headers={
                    "Content-Type": "application/json",
                    "Authorization": request.headers.get("Authorization")
                },
                request_params={"id": room_id},
                body=json.dumps({"location_hash": room_location_hash})
            )

            print("ROOM REGISTER: ", res, flush=True)
            
            if res.get("status"):
                return {
                    "status": True,
                    "msg": "room registered",
                    "room_hash": room_hash
                }, 200

            else:
                return {
                    "status": False,
                    "msg": "room register failed"
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
        return hashlib.sha256(
            str(request.remote_addr + room_hash).encode("utf-8")
        ).hexdigest()
            

    # get reservation at current time
    def get(self, room_id):
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

                room = room["room"]
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
        
