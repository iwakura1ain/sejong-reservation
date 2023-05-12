from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, desc

from config import db_config, model_config
from service import Service

import json


def serialize(row):
    return json.loads(json.dumps(dict(row), default=str))

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
    prefix="/reservation"
)


@ns.route("")
class ReservationList(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)

    def get(self):
        """
        Get a list of reservations
        - GET /reseration: 전체 예약 조회
        """

        # TODO: parse request.args
        # TODO: check user type info

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                stmt = select(Reservation)
                rows = conn.execute(stmt).mappings().fetchall()
                rows = [serialize(row) for row in rows]
            return {"status": True, "reservations": (rows)}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def post(self):
        """
        Make a new reservation
        - POST /reservation: New reservation with data
        """

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # insert new reservation
                new_reservation = request.json
                conn.execute(insert(Reservation), new_reservation)

                # select new reservation
                stmt = (select(Reservation)
                    .where(new_reservation["reservationTopic"] == Reservation.reservationTopic
                        and new_reservation["reservationDate"] == Reservation.reservationDate
                        and new_reservation["reservationType"] == Reservation.reservationType
                        and new_reservation["reservationRoom"] == Reservation.reservationRoom
                        and new_reservation["creator"] == Reservation.creator)
                    .order_by(desc(Reservation.createdAt)) # ORDER BY createdAt desc
                )
                rows = conn.execute(stmt).mappings().fetchall()
                # if duplicates with same contents exist, 
                # use the first one and delete the rest
                # TODO
                row = serialize(rows[0])
            return {"status": True, "reservation": row}, 200
        except Exception as e:
            return {"error": str(e)}, 400


@ns.route("/<int:id>", endpoint="aaaaa")
class ReservationByID(Resource, Service):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
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
            return row, 200
        except Exception as e:
            return {"status": False, "error": str(e)}, 400

    def patch(self, id: int):
        """
        Update a reservation
        - PATCH /reservation/1: id==1인 예약을 변경
        """

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # data to update
                update_data = request.json
                # TODO: data validation

                # update reservation
                stmt = (update(Reservation)
                    .where(Reservation.id == id)
                    .values(update_data))
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
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # delete reservation
                stmt = delete(Reservation).where(Reservation.id == id)
                conn.execute(stmt)
                return {"status": True, "msg": "deleted"}, 200

        # TODO: reservation with this ID does not exist
        except Exception as e:
            return {"status": False, "error": str(e)}, 400
