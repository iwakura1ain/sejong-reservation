from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, func

from config import model_config, api_config, MINIMIZED_COLS
from service import Service

from utils import (
    serialize,
    is_valid_token, is_admin, is_authorized,
    check_date_constraints,
    check_time_conflict,
)

import uuid

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
    prefix="/reservation"
)

@ns.route("")
class ReservationList(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config, api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    def get(self):
        """
        Get a list of reservations
        - GET /reseration: 전체 예약 조회
        - GET /reservation?before=2023-05-01: 2023-05-01 이전 예약 조회
        - GET /reservation?after=2023-05-01: 2023-05-01 이후 예약 조회
        - GET /reservation?room=센835: room_name이 "센835"인 회의실의 예약 조회
        """

        try:
            # get token info
            auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            # query parameters
            params = request.args

            with self.query_model("Reservation") as (conn, Reservation):
                stmt = None

                print("is_admin: ", is_admin(auth_info), flush=True)
                
                # return columns based on user type
                if is_admin(auth_info):  # full table
                    stmt = select(Reservation)
                else:  # only relevant columns
                    # TODO: ok?
                    select_cols = [
                        getattr(Reservation,col) for col in MINIMIZED_COLS
                    ]
                    stmt = select(select_cols)

                # filter by room id
                if room := params.get("room"):
                    stmt = stmt.where(Reservation.room_id == room)
                    
                # filter by creator id 
                if creator := params.get("creator"):
                    stmt = stmt.where(Reservation.creator_id == creator)
                    
                # filter by before date
                if before := params.get("before"):
                    stmt = stmt.where(Reservation.reservation_date <= before)

                # filter by after date
                if after := params.get("after"):
                    stmt = stmt.where(Reservation.reservation_date >= after)
                
                rows = conn.execute(stmt).mappings().fetchall()

                return {
                    "status": True,
                    "reservations": [serialize(row) for row in rows]
                }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Get reservation list failed."
            }, 400


    def post(self):
        """
        Make a new reservation
        - POST /reservation: New reservation with data
        """

        try:
            # get token info
            auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400
            
            reservations = request.json
            valid_reservaiton, invalid_reservaiton = [], []

            # make regular reservation uuid
            regular_reservation_uuid = None
            if len(reservations) > 1:
                regular_reservation_uuid = uuid.uuid4()

            with self.query_model("Reservation") as (conn, Reservation):
                for reservation in reservations:
                    # validate model
                    valid, invalid = Reservation.validate(reservation)
                    if invalid != {}:
                        return {
                            "status": False,
                            "msg": "Invalid reservation.",
                            "invalid": invalid
                        }, 400

                    user_type = auth_info["Uesr"]["type"]
                    reservation_date = valid["reservation_date"]
                    if not check_date_constraints(user_type, reservation_date):
                        return {
                            "status": False,
                            "msg": "User cannot reserve that far into future"
                        }, 400

                    # check rooms
                    room_id =valid["room"] 
                    room = self.query_api(
                        "get_rooms_info", "get", 
                        headers=request.headers, 
                        request_params={"id": room_id}
                    )
                    if not room["status"]:
                        return {
                            "status": False,
                            "msg": "Invalid room ID"
                        }, 400

                    if check_time_conflict(valid, connection=conn, model=Reservation):
                        invalid_reservaiton.append(valid)
                    
                if len(invalid_reservaiton) > 0:
                    return {
                        "status": False,
                        "msg": "Conflict in reservations",
                        "reservations":invalid_reservaiton
                    }

                # use regular_reservation_uuid for valid reservation
                valid["reservation_type"] = regular_reservation_uuid
                valid_reservaiton.append(valid)
                            
            # insert
            conn.execute(
                insert(Reservation).values(valid_reservaiton)
            )

            return {
                "status": True,
                "reservations": valid_reservaiton,
            }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Reservation failed."
            }, 400

@ns.route("/<int:id>")
class ReservationByID(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config,
                         api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    def get(self, id: int):
        """
        Read a reservation by reservation ID
        - GET /reservation/1:
            - id==1인 예약을 조회
        """

        try:
            # get token info
            auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            with self.query_model("Reservation") as (conn, Reservation):
                stmt = None

                print("is_admin: ", is_admin(auth_info), flush=True)
                
                # return columns based on user type
                if is_admin(auth_info):  # full table
                    stmt = select(Reservation)
                else:  # only relevant columns
                    # TODO: getattr ok?
                    select_cols = [
                        getattr(Reservation,col) for col in MINIMIZED_COLS
                    ]
                    stmt = select(select_cols)

                row = conn.execute(stmt).mappings().fetchone()

                # if reservation with this id doesn't exist
                if not row:
                    return {
                        "status": False,
                        "msg": "reservation not found"
                    }, 400

            return {
                "status": True,
                "reservation": serialize(row)
            }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Get reservation by ID failed."
            }, 400

    def patch(self, id: int):
        """
        Update a reservation
        - PATCH /reservation/1: id==1인 예약을 변경
        """

        try:
            # get token info
            auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            with self.query_model("Reservation") as (conn, Reservation):
                # validate model
                valid, invalid = Reservation.validate(request.json)
                if invalid != {}:
                    return {
                        "status": False,
                        "msg": "Invalid reservation.",
                        "invalid": invalid
                    }, 400

                # select updated reservation
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()

                # create updated and serialized reservation with validated values
                row.update(valid)

                user_type = auth_info["Uesr"]["type"]
                reservation_date = row["reservation_date"]
                if ("reservation_date" in valid.keys() 
                    and not check_date_constraints(user_type, reservation_date)):
                    return {
                        "status": False,
                        "msg": "User cannot reserve that far into future"
                    }, 400

                # check rooms
                if "room_id" in valid.keys():
                    room_id = row["room"] 
                    room = self.query_api(
                        "get_rooms_info", "get", 
                        headers=request.headers, 
                        request_params={"id": room_id}
                    )
                    if not room["status"]:
                        return {
                            "status": False,
                            "msg": "Invalid room ID"
                        }, 400

                if ("start_time" in valid.keys() and "end_time" in valid.keys()
                    and check_time_conflict(row, connection=conn, model=Reservation)):
                    return {
                        "status": False,
                        "msg": "Conflict in reservations"
                    }

                # update reservation
                stmt = (
                    update(Reservation)
                    .where(Reservation.id == id)
                    .values(valid)
                )
                conn.execute(stmt)
                
                # select updated reservation
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()
                
            return {
                "status": True,
                "reservation": serialize(row)
            }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Reservation edit failed."
            }, 400

    def delete(self, id: int):
        """
        Delete a reservation
        - DELETE /reservation/1: id==1인 예약을 삭제
        """

        # get token info
        auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
        if not is_valid_token(auth_info):
            return {
                "status": False,
                "msg": "Unauthenticated"
            }, 400
        
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # check if reservation with id exist.
                stmt = select(Reservation).where(Reservation.id == id)
                rows = conn.execute(stmt).mappings().fetchall()
                if len(rows) < 1:
                    return {
                        "status": False,
                        "msg": "room not found"
                    }, 400

                # authorized: creator, admin
                reservation = serialize(rows[0])
                # if not authorized to delete
                if not is_authorized(auth_info, reservation):
                    return {
                        "status": False,
                        "msg": "Unauthorized"
                    }, 400
                
                # delete reservation
                stmt = delete(Reservation).where(Reservation.id == id)
                conn.execute(stmt)

            return {
                "status": True,
                "msg": "Deleted"
            }, 200
            
        except Exception as e:
            return {
                "status": False,
                "msg": "server error"
            }, 400
