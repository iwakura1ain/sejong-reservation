from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, insert, update
from sqlalchemy import delete as remove

from openpyxl import load_workbook
from magic import Magic
from io import BytesIO

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
from utils import retrieve_jwt, serialize, protected, admin_only
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

    @jwt_required()
    @admin_only()
    def create_admin_user(*args, **kwargs):
        pass

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

                req, invalidated = User.validate(request.json)
                if len(invalidated) != 0:
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

                # hash password
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

        except OSError as e:
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

                req, invalidated = User.validate(request.json)
                if len(invalidated) != 0:
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
        
            
@AUTH.route("/import-users")
class UserImport(Service, Resource):
    allowed_filetypes = [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/x-ole-storage"
    ]

    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=ORM)
        Resource.__init__(self, *args, **kwargs)

    @jwt_required()
    @admin_only()
    def post(self):
        f = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if f.filename == '':
            return {
                "status": False,
                "msg": "no file selected"
            }, 200

        f = f.read()
        
        # check filetype
        mime = Magic(mime=True)
        if mime.from_buffer(f) not in self.allowed_filetypes:
            return {
                "status": False,
                "msg": "invalid filetype"
            }, 200

        with self.query_model("User") as (conn, User):
            users_sheet = load_workbook(filename=BytesIO(f)).active
            schema = User.columns

            insert_values = []
            for row in users_sheet.iter_rows(min_row=2, min_col=1, max_col=8):
                # create new user dict
                new_user, invalid = User.validate(
                    {key: val.value for key, val in zip(schema, row)}
                )

                #check excel values
                if len(invalid) != 0:
                    return {
                        "status": False,
                        "msg": "invalid value",
                        "invalid": row
                    }, 200

                # check if user in db 
                res = conn.execute(
                    select(User).where(User.id == new_user["id"])
                ).mappings().fetchone()
                if res is None:
                    new_user["password"] = generate_password_hash(new_user["password"])
                    insert_values.append(new_user)

            # insert new user
            conn.execute(
                insert(User), insert_values
            )

        return {
            "status": True,
            "msg": "users imported",
            "imported_count": len(insert_values)
        }, 200








