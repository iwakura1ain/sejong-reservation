from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete

from nanoid import generate

import json

from config import model_config, api_config, MINIMIZED_COLS
from service import Service

from utils import (
    serialize,
    is_valid_token, is_admin, is_authorized,
    check_date_constraints,
    check_time_conflict,
)

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
)


@ns.route("")
class ReservationList(Resource, Service):
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

    def get(self):
        """
        This function retrieves a list of reservations based on various filters such as date range and
        room name.

        :return: a JSON object with a "status" key indicating whether the request was successful or not,
        and a "reservations" key containing a list of reservation objects. The HTTP status code returned
        is either 200 for a successful request or 400 for a failed request.
        ---
        # Get a list of reservations
        # - GET /reseration: 전체 예약 조회
        # - GET /reservation?before=2023-05-01: 2023-05-01 이전 예약 조회
        # - GET /reservation?after=2023-05-01: 2023-05-01 이후 예약 조회
        # - GET /reservation?room=센835: room_name이 "센835"인 회의실의 예약 조회
        # - GET /reservation?from=2023-03-01&to=2023-06-01: 2023-03-01부터 2023-06-01까지 예약 조회. inclusive.
        """

        try:
            # get token info
            auth_info = self.query_api(
                "get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            with self.query_model("Reservation") as (conn, Reservation):
                stmt = None

                # return columns based on user type
                if is_admin(auth_info):  # full table
                    stmt = select(Reservation)
                # only relevant columns
                else:
                    select_cols = {
                        getattr(Reservation, col) for col in MINIMIZED_COLS
                    }
                    stmt = select(*select_cols)

                # query parameters
                params = request.args

                # filter by reservation_code (noshow code)
                if reservation_code := params.get("reservation_code"):
                    stmt = stmt.where(
                        Reservation.reservation_code == reservation_code
                    )

                # filter by reservation_type
                if reservation_type_ := params.get("reservation_type"):
                    stmt = stmt.where(
                        Reservation.reservation_type == reservation_type_)

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
                "msg": "Get reservation list failed"
            }, 400

    def post(self):
        """
        This function creates a new reservation and checks for conflicts and constraints before
        inserting it into the database.

        :return: a JSON object with a "status" key and a corresponding boolean value, as well as a "msg"
        key with a corresponding string value. The HTTP status code is also included in the return
        statement. If the reservation is successfully created, the function also includes a
        "reservation" key with a corresponding dictionary value containing information about the new
        reservation.
        """

        try:
            # get token info
            auth_info = self.query_api(
                "get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            reservations = request.json.get("reservations", [])

            # make regular reservation code
            reservation_type = generate(size=12) if len(
                reservations) > 1 else None
            valid_reservaitons, invalid_reservaitons = [], []
            with self.query_model("Reservation") as (conn, Reservation):
                for reservation in reservations:
                    # validate model
                    valid, invalid = Reservation.validate(reservation)
                    if invalid != {}:
                        return {
                            "status": False,
                            "msg": "Invalid reservation",
                            "invalid": invalid
                        }, 400
                    # if members data exist in valid, serialize to string for db
                    if "members" in valid.keys():
                        valid["members"] = json.dumps(valid["members"])

                    # check reservation date
                    reservation_date = valid["reservation_date"]
                    if not check_date_constraints(auth_info["User"]["type"], reservation_date):
                        return {
                            "status": False,
                            "msg": "User cannot reserve that far into future"
                        }, 400

                    # check room exists
                    room = self.query_api(
                        "get_rooms_info", "get",
                        headers=request.headers,
                        request_params={"id": valid["room_id"]}
                    )

                    print(room)
                    if "status" not in room.keys() or not room["status"]:
                        return {
                            "status": False,
                            "msg": "Invalid room ID"
                        }, 400

                    # check time conflict
                    if check_time_conflict(valid, connection=conn, model=Reservation):
                        # insert into invalid reservation list
                        invalid_reservaitons.append(valid)

                    else:
                        # insert reservation_type and reservation_code
                        valid["reservation_type"] = reservation_type
                        valid["reservation_code"] = generate(size=8)
                        # insert into valid reservation list
                        valid_reservaitons.append(valid)

                if len(invalid_reservaitons) > 0:
                    return {
                        "status": False,
                        "msg": "Conflict in reservations",
                        "reservations": [serialize(r) for r in invalid_reservaitons]
                    }

                # insert
                conn.execute(insert(Reservation), valid_reservaitons)

                # TODO: get inserted values from insert statement instead of selecting again
                retval = []
                for v in valid_reservaitons:
                    res = conn.execute(
                        select(Reservation)
                        .where(Reservation.reservation_code == v["reservation_code"])
                    ).mappings().fetchone()
                    retval.append(serialize(res))

            return {
                "status": True,
                "reservations": retval,
            }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Reservation failed"
            }, 400


@ns.route("/<int:id>")
class ReservationByID(Resource, Service):
    """
    The above code defines a Flask RESTful API endpoint for managing reservations. It includes methods
    for retrieving, updating, and deleting a reservation by its ID. The `get` method retrieves a
    reservation by its ID, the `patch` method updates a reservation by its ID, and the `delete` method
    deletes a reservation by its ID. The code also includes authorization checks to ensure that only
    authorized users can perform certain actions.
    """

    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, and takes in arguments for model and API configurations.
        """
        Service.__init__(self, model_config=model_config,
                         api_config=api_config)
        Resource.__init__(self, *args, **kwargs)

    def get(self, id: int):
        """
        This function retrieves a reservation by its ID and checks for authentication before returning
        the result.
        
        :param id: The parameter "id" is an integer that represents the ID of a reservation that needs
        to be retrieved.

        :return: a JSON object with the status of the request and either the reservation information or
        an error message. If the authentication token is invalid, it will return a status of False and
        an "Unauthenticated" error message. If the reservation ID is invalid, it will return a status of
        False and an "Invalid ID" error message. If the reservation is found, it will return a status of
        True and the found reservation data.
        """
        # Read a reservation by reservation ID
        # - GET /reservation/1:
        #     - id==1인 예약을 조회

        try:
            # get token info
            auth_info = self.query_api(
                "get_auth_info", "get", headers=request.headers)
            if not is_valid_token(auth_info):
                return {
                    "status": False,
                    "msg": "Unauthenticated"
                }, 400

            with self.query_model("Reservation") as (conn, Reservation):
                stmt = None

                # return columns based on user type
                if is_admin(auth_info):  # full table
                    stmt = select(Reservation)
                # only relevant columns
                else:
                    select_cols = {
                        getattr(Reservation, col) for col in MINIMIZED_COLS
                    }
                    stmt = select(*select_cols)

                row = conn.execute(stmt).mappings().fetchone()

                # if reservation with this id doesn't exist
                if not row:
                    return {
                        "status": False,
                        "msg": "Reservation not found"
                    }, 400

            return {
                "status": True,
                "reservation": serialize(row)
            }, 200

        except Exception as e:
            return {
                "status": False,
                "msg": "Get reservation by ID failed"
            }, 400

    def patch(self, id: int):
        """
        This function updates a reservation with the given ID, checking for conflicts and validating the
        input data.
        
        :param id: The id parameter is an integer that represents the unique identifier of a reservation
        that needs to be updated.

        :return: a dictionary with two keys: "status" and "reservation". The value of "status" is a
        boolean indicating whether the update was successful or not, and the value of "reservation" is a
        serialized row of the updated reservation. If there is an error, the function returns a
        dictionary with "status" set to False and a message indicating the error.
        """

        try:
            # get token info
            auth_info = self.query_api(
                "get_auth_info", "get", headers=request.headers)
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
                        "msg": "Invalid reservation",
                        "invalid": invalid
                    }, 400

                # select updated reservation
                stmt = select(Reservation).where(Reservation.id == id)
                row = conn.execute(stmt).mappings().fetchone()

                # create updated and serialized reservation
                # from RowMapping to dict with validated values
                row = serialize(row)
                row.update(**valid)

                reservation_date = row["reservation_date"]
                if ("reservation_date" in valid.keys()
                        and not check_date_constraints(auth_info["User"]["type"], reservation_date)):
                    return {
                        "status": False,
                        "msg": "User cannot reserve that far into future"
                    }, 400

                # check rooms
                if "room_id" in valid.keys():
                    room_id = row["room_id"]
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
                # if members data exist in data, serialize to string for db
                if "members" in row.keys():
                    row["members"] = json.dumps(row["members"])
                stmt = (
                    update(Reservation)
                    .where(Reservation.id == id)
                    .values(row)
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
                "msg": "Reservation edit failed"
            }, 400

    def delete(self, id: int):
        """
        This function deletes a reservation with a given ID if the user is authorized to do so.
        
        :param id: The id parameter is an integer that represents the unique identifier of the
        reservation that needs to be deleted.

        :return: a dictionary with keys "status" and "msg". The value of "status" indicates whether the
        deletion was successful or not, and the value of "msg" provides additional information about the
        status. The HTTP status code is also included in the return statement.
        """
        # Delete a reservation
        # - DELETE /reservation/1: id==1인 예약을 삭제

        # get token info
        auth_info = self.query_api(
            "get_auth_info", "get", headers=request.headers)
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
                        "msg": "Reservation not found"
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
                "msg": "Server error"
            }, 400
