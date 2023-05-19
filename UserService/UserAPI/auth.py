from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, insert, update
from sqlalchemy import delete as remove

from flask import request
from flask_restx import (
    Resource,
    fields,
    Namespace,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt
)

from service import Service
from utils import retrieve_jwt, serialize, protected
from config import ORM

# namespace for "/auth"
AUTH = Namespace(
    name="auth",
    description="사용자 인증을 위한 API",
)

# # required fields in request body?
# user_fields = auth.model('User', {
#     'username': fields.String(description='a User Name', required=True, example="justkode"),
#     'password': fields.String(description='Password', required=True, example="password")
# })

# # required fields in request body?
# jwt_fields = auth.model('JWT', {
#     'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
# })

include = ["id", "name", "type", "email", "no_show"]
exclude = ["password", "created_at"]



@AUTH.route('/register')
class Register(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    def post(self):
        """
        Endpoint for registering new users.
        ---
        request body:
        - username: new username
        - password: new password (currently has no length checks etc)
        """
        # using orm model
        try:
            with self.query_model("User") as (conn, User):
                # validate request body arguments
                req, status = User.validate(request.json)
                if not status:
                    return {
                        "status": False,
                        "msg": "key:value pair wrong"
                    }, 200

                # check if user exists
                res = conn.execute(
                    select(User).where(User.id == req["id"])
                ).mappings().all()

                if len(res) != 0:
                    return {
                        "status": False,
                        "msg": "User Exists"
                    }, 200

                req["password"] = generate_password_hash(req["password"])
                
                # create new user
                conn.execute(
                    insert(User), {
                        **req
                    }
                )

                # return new user
                res = conn.execute(
                    select(User).where(User.id == req["id"])
                ).mappings().fetchone()

                return {
                    "status": True,
                    "msg": "success",
                    "User": serialize(res, exclude=exclude)
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "Register Failed",
            }, 500


@AUTH.route('/login')
class Login(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    def post(self):
        """
        Endpoint for loging in users
        ---
        req body:
        - username: existing username
        - password: plaintext password
        """
        
        # using orm model
        try:
            with self.query_model("User") as (conn, User):
                # validate request body
                req, status = User.validate(request.json)
                if not status:
                    return {
                        "status": False,
                        "msg": "key:value pair wrong"
                    }, 200

                # get user
                res = conn.execute(
                    select(User).where(User.id == req["id"])
                ).mappings().fetchone()

                # check if user exists
                if res is None:
                    return {
                        "status": False,
                        "msg": "User Not Found"
                    }, 200

                # check if password is right
                if not check_password_hash(res["password"], req["password"]):
                    return {
                        "status": False,
                        "msg": "Wrong Password"
                    }, 200

                # TODO: replace names with underscore names
                identity = serialize(res, include=include)
                access_token = create_access_token(
                    identity=identity,
                    fresh=True
                )
                refresh_token = create_refresh_token(
                    identity=identity
                )
                
                return {
                    "status": True,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "User": serialize(res, exclude=exclude)
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "Login Failed"
            }, 500

@AUTH.route('/logout')
class Logout(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    
    def add_token_to_blocklist(self, token):
        # from config import TOKEN_BLOCKLIST
        
        # if jti not in TOKEN_BLOCKLIST:
        #     TOKEN_BLOCKLIST.add(jti)
        #     return True
        # return False
        with self.query_model("Token_Blocklist") as (conn, Blocklist):
            res = conn.execute(
                select(Blocklist).where(Blocklist.jti == token["jti"])
            ).mappings().fetchone()
            if res is not None:
                return False

            res = conn.execute(
                insert(Blocklist),
                {
                    "jti": token["jti"],
                    "user_id": token["sub"]["id"],
                    "type": token["sub"]["type"]
                }
            )
            return True

    @jwt_required(verify_type=False)
    def delete(self):
        """
        Logout User.
        """
        jwt = get_jwt()
        if self.add_token_to_blocklist(jwt):
            return {
                "status": True,
                "msg": "token revoked"
            }
        return {
            "status": True,
            "msg": "already revoked"
        }

@AUTH.route("/jwt-status")
class JWTStatus(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    def get(self):
        """
        Endpoint for checking if user token is valid.
        ---
        req header
        - Authentication: Bearer [JWT Token]
        """
        try:             
            with self.query_model("User") as (conn, User):
                identity = retrieve_jwt()
                res = conn.execute(
                    select(User).where(User.id == identity["id"])
                ).mappings().fetchone()

                return {
                    "status": True,
                    "msg": "authenticated",
                    "User": serialize(res, exclude=exclude)
                }, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "msg": "jwt status Failed"
            }, 500


@AUTH.route("/jwt-refresh")
class JWTRefresh(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required(refresh=True)
    def get(self):
        """
        Endpoint for checking if user token is valid.
        ---
        req header
        - Authentication: Bearer [JWT Token]
        """
        identity = retrieve_jwt()
        access_token = create_access_token(identity=identity)
        return {
            "status": True,
            "access_token": access_token,
        }, 200
        
            
    




