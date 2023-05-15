from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, func

from config import model_config, api_config
from service import Service

import json
from datetime import date, time, timedelta


def serialize(row):
    return json.loads(json.dumps(dict(row), default=str))

def is_valid_token(auth_info):
    if auth_info["msg"] == "Token has expired" \
        or auth_info["status"] == False:
        return False
    return True

# user info
def is_admin(auth_info):
    #TODO 관리자가 아니더라도 user가 관리하는 방이면 관리자급 조회가능하도록?
    if auth_info["User"]["type"] == 1:
        return True
    return False

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
    prefix="/reservation"
)


@ns.route("")
class ReservationList(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(
            self, 
            model_config=model_config,
            api_config=api_config
        )
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
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400

        # parse request.args
        before = request.args.get("before")
        after = request.args.get("after")
        room = request.args.get("room") 
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
                    stmt = select(Reservation.id, Reservation.reservation_date,
                        Reservation.start_time, Reservation.end_time, Reservation.which_room)

                # filter by dates
                if range_from and range_to:
                    stmt = (stmt.where(Reservation.reservation_date >= range_from)
                        .where(Reservation.reservation_date <= range_to))

                if before:
                    stmt = stmt.where(Reservation.reservation_date <= before)
                if after:
                    stmt = stmt.where(Reservation.reservation_date >= after)
                # filter by room
                if room:
                    room_id = None # self.query_api to get room id.
                    stmt = stmt.where(Reservation.which_room == room_id)

                rows = conn.execute(stmt).mappings().fetchall()
                rows = [serialize(row) for row in rows]
            return {"status": True, "reservations": rows}, 200
        except Exception as e:
            return {"status": False, "msg":"Unauthenticated"}, 400

    def post(self):
        """
        Make a new reservation
        - POST /reservation: New reservation with data
        """

        # get token info
        auth_info = self.query_api("get_auth_info","get",headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400

        new_reservation = request.json
        #TODO: generate code for a new reservation

        # check date constraints. prof unlimited, grad=1week, undergrad=2days, undergrad=no multiple reserv.
        diff = date.today() - date.fromisoformat(new_reservation["reservation_date"])
        if auth_info["User"]["type"] == 1 or auth_info["User"]["type"] == 2:
            pass
        elif auth_info["User"]["type"] == 3 and diff > timedelta(weeks=1):
            return {"status": False, "msg": "User(grad) cannot make reservation for this date"}
        elif auth_info["User"]["type"] == 4 and diff > timedelta(days=2):
            return {"status": False, "msg": "User(undergrad) cannot make reservation for this date"}

        # check if start < end
        if new_reservation["start_time"] > new_reservation["end_time"]:
            return {"status": False, "msg": "End time earlier than start time"}

        # check if start_time, end_time within open hours
        if time.fromisoformat(new_reservation["start_time"]) < time(9,0) \
            or time.fromisoformat(new_reservation["end_time"]) > time(18,0):
            return {"status": False, "msg": "Open hours: 0900~1800"}

        # # check if room valid
        # TODO: use requests library GET /admin/rooms/1

        # reservation_topic string len check
        if len(new_reservation["reservation_topic"]) > 100:
            return {"status": False, "msg": "reservation topic is too long"}

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # validate model
                new_reservation = Reservation.validate(request.json)

                # check time conflict
                new_start_time = new_reservation["start_time"]
                new_end_time = new_reservation["end_time"]
                stmt = (select(Reservation.id, Reservation.reservation_date, 
                    Reservation.start_time, Reservation.end_time, Reservation.which_room)
                    .where(Reservation.reservation_date == new_reservation["reservation_date"])
                    .where(Reservation.which_room == new_reservation["which_room"])
                    .filter(func.time(Reservation.start_time).between(new_start_time, new_end_time)))
                rows = conn.execute(stmt).mappings().fetchall()
                time_conflict_rows = [serialize(row) for row in rows]

                # if time conficts exist, return conflicting rows
                if len(time_conflict_rows) > 0:
                    return {"status": False, "msg":"Time conflict",
                        "reservations":time_conflict_rows}, 400

                # insert new reservation
                conn.execute(insert(Reservation), new_reservation)

                # select new reservation
                # TODO: check if same reservation exist
                stmt = (select(Reservation)
                    .where(Reservation.which_room == new_reservation["which_room"])
                    .where(Reservation.start_time == new_reservation["start_time"])
                    .where(Reservation.end_time == new_reservation["end_time"]))
                rows = conn.execute(stmt).mappings().fetchall()
                # if duplicates with same contents exist, use only the first one and delete the rest
                if len(rows)>1:
                    # delete rows[1:]
                    pass
                row = serialize(rows[0])
                return {"status": True, "msg":"Success", "reservation": row}, 200
        except Exception as e:
            return {"status":False, "msg":"Reservation failed"}, 400


@ns.route("/<int:id>")
class ReservationByID(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(
            self, 
            model_config=model_config,
            api_config=api_config
        )
        Resource.__init__(self, *args, **kwargs)

    def get(self, id: int):
        """
        Read a reservation by reservation ID
        - GET /reservation/1:
            - id==1인 예약을 조회
        """
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                stmt = select(Reservation).where(Reservation.id==id)
                row = conn.execute(stmt).mappings().fetchone()
                row = serialize(row)
            return {"status":True, "reservation":row}, 200
        except Exception as e:
            return {"status":False, "msg":"No ..."}, 400

    def patch(self, id: int):
        """
        Update a reservation
        - PATCH /reservation/1: id==1인 예약을 변경
        """
        # data to update
        upd_reservation = request.json
        # if not authorized to delete, return
        # authorized: creator, admin?
        # TODO: data validation
        try:
            with self.query_model("Reservation") as (conn, Reservation):
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
            return {"status": False, "error": str(e)}, 400

    def delete(self, id: int):
        """
        Delete a reservation
        - DELETE /reservation/1: id==1인 예약을 삭제
        """
        # if not authorized to delete, return
        # authorized: creator, admin
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # TODO: first, check if reservation with id exist.
                # delete reservation
                stmt = delete(Reservation).where(Reservation.id == id)
                conn.execute(stmt)
                return {"status": True, "msg": "deleted"}, 200

        # TODO: reservation with this ID does not exist
        except Exception as e:
            return {"status": False, "error": str(e)}, 400
