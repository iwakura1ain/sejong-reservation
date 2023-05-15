from sqlalchemy import select, insert, update
from sqlalchemy import delete as remove

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


# namespace for "/auth"
USERS = Namespace(
    name="users",
    description="사용자 CRUD 위한 API",
)

exclude = ["password"]

@USERS.route("")
class UserList(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    @protected()
    def get(self):
        """
        Get user list.
        """
        try:
            with self.query_model("Users") as (conn, User):
                res = conn.execute(
                    select(User)
                ).mappings().all()

                return {
                    "status": True,
                    "Users": [serialize(r, exclude=exclude) for r in res]
                }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "error"
            }, 500


@USERS.route("/<id>")
class UserDetail(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    @protected()
    def get(self, id):
        """
        Get user info
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
        Modify user
        """
        try:
            with self.query_model("User") as (conn, User):
                req = User.validate(request.json)

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
        Delete User
        """
        try:
            with self.query_model("User") as (conn, User):
                conn.execute(
                    remove(User).where(User.id == id)
                )

                return {
                    "status": True,
                    "msg": "deleted"
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "error"
            }, 200


                

        


