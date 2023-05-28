from sqlalchemy import select, insert, update
from sqlalchemy import delete as remove

from werkzeug.security import check_password_hash, generate_password_hash

from flask import request
from flask_restx import (
    Resource,
    fields,
    Namespace,
    Api
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required
)



from service import Service
from utils import retrieve_jwt, serialize, protected
from config import ORM

"""
This code creates a Flask-RestX namespace object called "USERS" for handling CRUD (Create, Read,
Update, Delete) operations related to users in an API. The namespace is assigned a name "users" and
a description "사용자 CRUD 위한 API" (which means "API for user CRUD" in Korean).
"""


# namespace for "/users"
USERS = Namespace(
    name="users",
    description="사용자 CRUD 위한 API",
)

exclude = ["password", "created_at"]

@USERS.route("")
class UserList(Service, Resource):
    """
    This is a Python class that defines a resource for getting a list of users, with authentication and
    serialization.
    """

    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing ORM as a model configuration parameter to the Service class.
        """
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    @protected()
    def get(self):
        """
        This function retrieves a list of users and returns it as a serialized JSON object, while also
        handling exceptions.
        
        :return: A dictionary is being returned with the keys "status" and "Users". The value of
        "status" is a boolean indicating whether the operation was successful or not, and the value of
        "Users" is a list of serialized user objects. If an exception occurs, a dictionary with the keys
        "status" and "msg" is returned instead.
        """

        try:
            with self.query_model("User") as (conn, User):
                stmt = select(User)

                params = request.args
                if user_type := params.get("user_type"):
                    stmt = stmt.where(User.type == user_type)

                if dept := params.get("dept"):
                    stmt = stmt.where(User.dept == dept)
                    
                if order_by := params.get("order_by"):
                    col = getattr(User, order_by)
                    stmt = stmt.order_by(col)

                if count := request.args.get("count"):
                    stmt = stmt.limit(count)

                res = conn.execute(stmt).mappings().fetchall()
                return {
                    "status": True,
                    "Users": [serialize(r, exclude=exclude) for r in res]
                }

        except Exception as e:
            print(e, flush=True)
            return {
                "status": False,
                "msg": "error"
            }, 500


@USERS.route("/<string:id>")
class UserDetail(Service, Resource):
    """
    This code defines a Flask-RestX resource for handling CRUD operations related to a specific user
    identified by their `id`. The resource includes three methods: `get`, `patch`, and `delete`.
    """
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing ORM as a model configuration parameter to the Service class.
        """
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    @protected()
    def get(self, id):
        """
        This function retrieves user information with authentication and protection using JWT.
        
        :param id: The parameter "id" is the unique identifier of the user whose information is being
        retrieved

        :return: This code defines a GET endpoint for retrieving user information. If the user with the
        specified ID exists in the database, the endpoint returns a JSON response with a "status" key
        set to True, a "msg" key set to "retrieved", and a "User" key set to the serialized user object.
        If the user does not exist, the endpoint returns a JSON response with a error message."
        """
        try:
            with self.query_model("User") as (conn, User):
                res = conn.execute(
                    select(User).where(User.id == id)
                ).mappings().fetchone()

                if res is None:
                    return {
                        "status": False,
                        "msg": "no user"
                    }, 200

                return {
                    "status": True,
                    "msg": "retrieved",
                    "User": serialize(res, exclude=exclude)
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "error"
            }, 200

    @jwt_required()
    @protected()
    def patch(self, id):  # TODO: differenciate what admins and users can change
        """
        This is a Python function that modifies a user's information and returns a response with the
        updated user data.
        
        :param id: The id parameter is the unique identifier of the user that needs to be modified
        :return: a JSON response with a status message and the updated user information in case of
        success, or an error message in case of failure. The status message indicates whether the update
        was successful or not.
        """
        try:
            with self.query_model("User") as (conn, User):
                req, invalidated = User.validate(request.json, optional=True, drop=True)
                if len(invalidated) != 0:
                    return {
                        "status": False,
                        "msg": "key:value pair wrong"
                    }, 200
                
                res = conn.execute(
                    select(User).where(User.id == id)
                ).mappings().fetchone()
                if len(res) == 0:
                    return {
                        "status": False,
                        "msg": "user not found"
                    }, 200

                if "password" in req.keys():
                    req["password"] = generate_password_hash(req["password"])

                conn.execute(
                    update(User).where(User.id == id).values(**req)
                )

                res = conn.execute(
                    select(User).where(User.id == id)
                ).mappings().fetchone()

                return {
                    "status": True,
                    "msg": "updated",
                    "User": serialize(res, exclude=exclude)
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "error"
            }, 200

    @jwt_required()
    @protected()
    def delete(self, id):  # TODO: differenciate what admins and users can change
        """
        This function deletes a user with a given ID, and returns a success message if the deletion was
        successful.
        
        :param id: The id parameter is the unique identifier of the user that needs to be deleted
        :return: A dictionary containing a status and message, along with an HTTP status code. If the
        deletion is successful, the status will be True and the message will be "deleted", with an HTTP
        status code of 200. If there is an error, the status will be False and the message will be
        "error", with an HTTP status code of 200.
        """
        try:
            # with self.query_model("User") as (conn, User):
            #     res = conn.execute(
            #         select(User).where(User.id == id)
            #     ).mappings().fetchone()
            #     if len(res) == 0:
            #         return {
            #             "status": False,
            #             "msg": "user not found"
            #         }, 200

            with self.query_model("Token_Blocklist") as (conn, Blocklist):
                conn.execute(
                    remove(Blocklist).where(Blocklist.id == id)
                )
            
            with self.query_model("User") as (conn, User):
                res = conn.execute(
                    select(User).where(User.id == id)
                ).mappings().fetchone()

                if len(res) == 0:
                    return {
                        "status": False,
                        "msg": "user not found"
                    }, 200

                conn.execute(
                    remove(User).where(User.id == id)
                )

                return {
                    "status": True,
                    "msg": "deleted"
                }, 200

            #TODO: must revoke current token from user

        except OSError as e:
            print(e)
            return {
                "status": False,
                "msg": "error while deleting user"
            }, 200



@USERS.route("/<string:id>/no-show")
class UserNoShowIncrement(Service, Resource):
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from both Service and Resource
        classes, passing ORM as a model configuration parameter to the Service class.
        """
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    def post(self, id):
        noshow_count = request.json.get("noshow_count")
        if noshow_count is None:
            return {
                "status": False,
                "msg": "wrong key:value pair"
            }, 200
            
        with self.query_model("User") as (conn, User):
            res = conn.execute(
                select(User).where(User.id == id)
            ).mappings().fetchone()

            if res is None:
                return {
                    "status": False,
                    "msg": "User not found"
                }, 200

            noshow_count = res["no_show"] + noshow_count

            conn.execute(
                update(User).where(User.id == id)
                .values(no_show=noshow_count)
            )

            return {
                "status": True,
                "msg": "User noshow incremented"
            }, 200

