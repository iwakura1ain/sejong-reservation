from flask import request
from flask_restx import Resource, Namespace

from sqlalchemy import select, insert, update, delete, func

import json
from datetime import date, time, timedelta

from config import model_config, api_config
from service import Service

def serialize(row):
    """
    The function serializes a row by converting it into a dictionary and then into a JSON object with
    string representation of non-serializable values.

    :param row: The parameter "row" is likely a dictionary or a row object from a database query result.

    :return: The function `serialize` is returning a dictionary that is created by converting the input
    `row` into a JSON string using `json.dumps`, and then converting that JSON string back into a
    dictionary using `json.loads`. The `default=str` argument is used to ensure that any
    non-serializable values in the `row` dictionary are converted to strings before being serialized.
    """
    return json.loads(json.dumps(dict(row), default=str))


def is_valid_token(auth_info):
    """
    The function checks if a token is valid by verifying if the "status" key is present in the
    authentication information dictionary.

    :param auth_info: The auth_info parameter is a dictionary that contains information about an
    authentication token. 

    :return: a boolean value. If the "status" key is not present in the input dictionary "auth_info", it
    returns False. Otherwise, it returns the value associated with the "status" key, which is expected
    to be a boolean value indicating whether the token is valid or not.
    """
    if "status" not in auth_info.keys():
        return False
    return auth_info["status"]


def is_admin(auth_info):
    """
    The function checks if the user is an admin based on their authentication information.

    :param auth_info: It is a dictionary containing information about the user's authentication status.
    It includes information such as the user's ID, username, and the type of account (e.g. regular
    user or administrator).

    :return: a boolean value indicating whether the user is an admin or not. If the user is an admin,
    the function returns True, otherwise it returns False.
    """
    # TODO 관리자가 아니더라도 user가 관리하는 방이면 관리자급 조회가능하도록?
    if auth_info["User"]["type"] == 2:
        return True
    return False


def check_time_conflict(conn, Reservation, new_reservation):
    """
    This function checks for time conflicts between a new reservation and existing reservations in a
    database.

    :param conn: The database connection object used to execute the SQL query.

    :param Reservation: The Reservation parameter is a SQLAlchemy Table object representing a
    table in a database that stores information about reservations, such as the reservation date, start
    time, end time, and which room the reservation is for.

    :param new_reservation: The new reservation that needs to be checked for time conflicts with
    existing reservations.

    :return: a list of serialized rows from the database that represent any existing reservations that
    conflict with the new reservation being passed in as an argument.
    """
    new_start_time = new_reservation["start_time"]
    new_end_time = new_reservation["end_time"]
    stmt = (select(Reservation.id, Reservation.reservation_date,
        Reservation.start_time, Reservation.end_time, Reservation.which_room)
        .where(Reservation.reservation_date == new_reservation["reservation_date"])
        .where(Reservation.which_room == new_reservation["which_room"])
        .filter(func.time(Reservation.start_time).between(new_start_time, new_end_time))
        .filter(func.time(Reservation.end_time).between(new_start_time, new_end_time)))
    rows = conn.execute(stmt).mappings().fetchall()
    return [serialize(row) for row in rows]


def check_start_end_time(new_reservation):
    """
    This function checks the validity of a reservation's start and end times, ensuring they are within
    open hours and the start time is earlier than the end time.

    :param new_reservation: A dictionary containing information about a new reservation, including the
    start time and end time.

    :return: either a string indicating an error message if the reservation's start_time is later than
    the end_time or if the reservation is not within the open hours, or it returns None if the
    reservation's start_time and end_time are valid and within the open hours.
    """
    # check if start < end
    if new_reservation["start_time"] > new_reservation["end_time"]:
        return "End time earlier than start time"
    # check if start_time, end_time within open hours
    if time.fromisoformat(new_reservation["start_time"]) < time(9, 0) \
        or time.fromisoformat(new_reservation["end_time"]) > time(18, 0):
        return "Open hours: 0900~1800"
    return None


# check date constraints
def check_date_constraints(auth_info, new_reservation):
    """
    This function checks if a user is authorized to make a reservation based on their user type and the
    reservation date constraints.

    :param auth_info: A dictionary containing information about the user making the reservation,
    including their user type.

    :param new_reservation: A dictionary containing information about a new reservation, including the
    reservation date in ISO format (YYYY-MM-DD).

    :return: a string message if the date constraints are not met based on the user type, otherwise it
    returns None.
    """
    diff = date.today() - date.fromisoformat(new_reservation["reservation_date"])
    if auth_info["User"]["type"] == 1 or auth_info["User"]["type"] == 2:
        pass
    elif auth_info["User"]["type"] == 3 and diff > timedelta(weeks=1):
        return "User(grad) cannot make reservation for this date"
    elif auth_info["User"]["type"] == 4 and diff > timedelta(days=2):
        return "User(undergrad) cannot make reservation for this date"
    return None


def is_authorized(auth_info, reservation):
    """
    The function checks if a user is authorized to access a reservation based on their authentication
    information and the reservation's creator ID.

    :param auth_info: A dictionary containing information about the user who is trying to access the
    reservation. It includes the user's ID and type (1 for regular user, 2 for admin).

    :param reservation: The reservation is a dictionary that contains information about a reservation,
    such as the creator_id, start time, end time, and other relevant details.

    :return: a boolean value indicating whether the user is authorized to access the reservation or not.
    True is returned if the user is the creator of the reservation or an admin, and False is returned
    otherwise.
    """
    user = auth_info["User"]
    # user is creator of reservation
    if user["id"] == reservation["creator_id"]:
        return True
    # user is admin
    if user["type"] == 2:
        return True
    return False

ns = Namespace(
    name="reservation",
    description="예약 서비스 API",
    prefix="/reservation"
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
        """
        # Get a list of reservations
        # - GET /reseration: 전체 예약 조회
        # - GET /reservation?before=2023-05-01: 2023-05-01 이전 예약 조회
        # - GET /reservation?after=2023-05-01: 2023-05-01 이후 예약 조회
        # - GET /reservation?room=센835: room_name이 "센835"인 회의실의 예약 조회
        # - GET /reservation?from=2023-03-01&to=2023-06-01: 2023-03-01부터 2023-06-01까지 예약 조회. inclusive.

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
        This function creates a new reservation and checks for conflicts and constraints before
        inserting it into the database.

        :return: a JSON object with a "status" key and a corresponding boolean value, as well as a "msg"
        key with a corresponding string value. The HTTP status code is also included in the return
        statement. If the reservation is successfully created, the function also includes a
        "reservation" key with a corresponding dictionary value containing information about the new
        reservation.
        """
        # Make a new reservation
        # - POST /reservation: New reservation with data
        # get token info
        auth_info = self.query_api("get_auth_info", "get", headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400

        new_reservation = request.json
        #TODO: generate code for a new reservation

        msg = check_date_constraints(auth_info, new_reservation)
        if msg:
            return {"status": False, "msg": msg}, 400

        msg = check_start_end_time(new_reservation)
        if msg:
            return {"status": False, "msg": msg}, 400
        
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
                time_conflict_rows = check_time_conflict(conn, Reservation, new_reservation)
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
                    # TODO: delete rows[1:]
                    pass
                row = serialize(rows[0])
            return {"status":True, "reservation":row}, 200
        except Exception as e:
            return {"status":False, "msg":"Reservation failed"}, 400


"""
The above code defines a Flask RESTful API endpoint for managing reservations. It includes methods
for retrieving, updating, and deleting a reservation by its ID. The `get` method retrieves a
reservation by its ID, the `patch` method updates a reservation by its ID, and the `delete` method
deletes a reservation by its ID. The code also includes authorization checks to ensure that only
authorized users can perform certain actions.
"""
@ns.route("/<int:id>")
class ReservationByID(Resource, Service):
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

        # get token info
        auth_info = self.query_api("get_auth_info","get",headers=request.headers)
        if not is_valid_token(auth_info):
            return {"status": False, "msg":"Unauthenticated"}, 400

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                stmt = select(Reservation).where(Reservation.id==id)
                row = conn.execute(stmt).mappings().fetchone()
                row = serialize(row)

            return {"status":True, "reservation":row}, 200
        except Exception as e:
            return {"status":False, "msg":"Invalid ID"}, 400

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
        # Update a reservation
        # - PATCH /reservation/1: id==1인 예약을 변경
        # data to update
        upd_reservation = request.json
        # if not authorized to delete, return
        # authorized: creator, admin?

        msg = check_start_end_time(upd_reservation)
        if msg:
            return {"status": False, "msg": msg}

        try:
            with self.query_model("Reservation") as (conn, Reservation):
                # validate model
                upd_reservation = Reservation.validate(request.json)

                # check time conflict
                time_conflict_rows = check_time_conflict(conn, Reservation, upd_reservation)
                # if time conficts exist, return conflicting rows
                if len(time_conflict_rows) > 0:
                    return {"status": False, "msg":"Time conflict",
                        "reservations":time_conflict_rows}, 400

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
            return {"status":False, "msg":"Invalid ID"}, 400

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
        auth_info = self.query_api("get_auth_info","get",headers=request.headers)
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