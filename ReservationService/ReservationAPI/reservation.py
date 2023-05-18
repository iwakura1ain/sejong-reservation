from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, func

from config import model_config, api_config
from service import Service
# from validators import start_end_time_validator

from utils import (
    serialize,
    is_valid_token, is_admin, is_authorized,
    # check_start_end_time, 
    check_date_constraints, 
    check_time_conflict,
)

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
    prefix="/reservation"
)

@ns.route("")
class ReservationList(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config,
                         api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    def get(self):
        """
        Get a list of reservations
        - GET /reseration: 전체 예약 조회
        - GET /reservation?before=2023-05-01: 2023-05-01 이전 예약 조회
        - GET /reservation?after=2023-05-01: 2023-05-01 이후 예약 조회
        - GET /reservation?room=센835: room_name이 "센835"인 회의실의 예약 조회
        - GET /reservation?from=2023-03-01&to=2023-06-01: 2023-03-01부터 2023-06-01까지 예약 조회. inclusive.
        """

        # get token info
        auth_info = self.query_api("get_auth_info","get",headers=request.headers)
        if not auth_info["status"]:
            return {"status": False, "msg":"Unauthenticated"}, 400

        # parse request.args
        # TODO: use validators
        before = request.args.get("before")
        after = request.args.get("after")
        room_name = request.args.get("room") 
        range_from = request.args.get("from")
        range_to = request.args.get("to")

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                stmt = None
                # full table
                if is_admin(auth_info): 
                    stmt = select(Reservation)
                # only relavent columns
                else: 
                    stmt = select(Reservation.id, 
                        Reservation.reservation_date, 
                        Reservation.reservation_type,
                        Reservation.start_time, Reservation.end_time, Reservation.room_id)

                # filter by dates
                if range_from and range_to:
                    stmt = (stmt.where(Reservation.reservation_date >= range_from)
                        .where(Reservation.reservation_date <= range_to))
                if before:
                    stmt = stmt.where(Reservation.reservation_date <= before)
                if after:
                    stmt = stmt.where(Reservation.reservation_date >= after)

                # filter by room
                if room_name:
                    rooms = self.query_api("get_rooms_info","get",headers=request.headers)
                    rooms = rooms["allRooms"]
                    room_id = None
                    for room in rooms:
                        if room["room_name"] == room_name:
                            room_id = room["id"]
                            break
                    if not room_id:
                        return {"status": False, "msg":"Invalid room ID."}, 400
                    stmt = stmt.where(Reservation.room_id == room_id)

                rows = conn.execute(stmt).mappings().fetchall()
                rows = [serialize(row) for row in rows]
            return {"status": True, "reservations": rows}, 200

        except Exception as e:
            return {"status": False, "msg":f"Get reservation failed. {e}"}, 400


    # @start_end_time_validator
    def post(self):
        """
        Make a new reservation
        - POST /reservation: New reservation with data
        """
        #TODO: generate code for a new reservation

        # get token info
        auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400
        
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # validate model
                new_reservation, invalid = Reservation.validate(request.json)
                if invalid:
                    return {"status": False, "msg": f"Invalid reservation. {invalid}"}, 400
                import sys; print(new_reservation, invalid, file=sys.stderr)

                msg = check_date_constraints(auth_info, new_reservation)
                if msg:
                    return {"status": False, "msg": msg}, 400

                # check if room is valid
                rooms = self.query_api("get_rooms_info","get",headers=request.headers)
                room_ids = [room["id"] for room in rooms["allRooms"]]
                if new_reservation["room_id"] not in room_ids:
                    return {"status": False, "msg":"Invalid room ID."}, 400

                # check time conflict
                time_conflict_rows = check_time_conflict(conn, Reservation, new_reservation)
                # if time conficts exist, return conflicting rows
                if len(time_conflict_rows) > 0:
                    return {"status": False, "msg":"Time conflict",
                        "reservations":time_conflict_rows}, 400

                # insert new reservation
                conn.execute(insert(Reservation), new_reservation)
            return {"status":True, "reservation":new_reservation}, 200

        except Exception as e:
            return {"status":False, "msg":f"Reservation failed. {e}"}, 400


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

        # get token info
        auth_info = self.query_api("get_auth_info","get",headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # TODO: give less info if user is not owner...
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()
                # if reservation with this id doesn't exist
                if not row:
                    return {"status":False, "msg":"Invalid ID."}, 400

                reservation = serialize(row)
            return {"status":True, "reservation":reservation}, 200

        except Exception as e:
            return {"status":False, "msg":f"Get reservation by ID failed. {e}"}, 400

    def patch(self, id: int):
        """
        Update a reservation
        - PATCH /reservation/1: id==1인 예약을 변경
        """

        # if not authorized to delete, return
        # TODO: authorized: creator, admin?
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # check if reservation with id exist.
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()
                if not row:
                    return {"status": False, "msg": "Invalid ID"}, 400
                
                # update serialized reservation with validate model
                upd_reservation = serialize(row)
                upd_reservation.update(request.json)
                upd_reservation,invalid = Reservation.validate(upd_reservation)
                if invalid:
                    return {"status": False, "msg": f"Invalid reservation. {invalid}"}, 400

                # check time conflict
                time_conflict_rows = check_time_conflict(conn, Reservation, upd_reservation)
                # if there is only one conflict with the same id, pass
                if len(time_conflict_rows) == 1 and time_conflict_rows[0]["id"] == id:
                    pass
                # if time conficts exist, return conflicting rows
                elif len(time_conflict_rows) > 0:
                    return {"status": False, "msg":"Time conflict",
                        "reservations":time_conflict_rows}, 400

                # # check start, end times 
                # msg = check_start_end_time(upd_reservation)
                # if msg:
                #     return {"status": False, "msg": msg}

                # update reservation
                stmt = (update(Reservation)
                    .where(Reservation.id == id)
                    .values(upd_reservation))
                conn.execute(stmt)
                # select updated reservation
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()
                row = serialize(row)
            return {"status": True, "reservation": row}, 200

        except Exception as e:
            return {"status":False, "msg":f"Reservation edit failed. {e}"}, 400

    def delete(self, id: int):
        """
        Delete a reservation
        - DELETE /reservation/1: id==1인 예약을 삭제
        """

        # get token info
        auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400
        
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # check if reservation with id exist.
                stmt = select(Reservation).where(Reservation.id == id)
                rows = conn.execute(stmt).mappings().fetchall()
                if len(rows) < 1:
                    return {"status": False, "msg": "Invalid ID"}, 400

                # authorized: creator, admin
                reservation = serialize(rows[0])
                # if not authorized to delete
                if not is_authorized(auth_info, reservation):
                    return {"status": False, "msg":"Unauthorized"}, 400
                
                # delete reservation
                stmt = delete(Reservation).where(Reservation.id == id)
                conn.execute(stmt)
            return {"status": True, "msg": "Deleted"}, 200
            
        except Exception as e:
            return {"status":False, "msg":"Invalid ID"}, 400
