# import jwt
# from jwt.exceptions import DecodeError

from flask import g, request
from flask_restx import Resource, fields, Namespace, Api
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
)

from werkzeug.security import check_password_hash, generate_password_hash

#from db import get_db, get_cur
from service import Service, validator


from sqlalchemy import select, insert


# namespace for "/auth"
auth = Namespace(
    name="auth",
    description="사용자 인증을 위한 API",
)

# required fields in request body?
user_fields = auth.model('User', { 
    'username': fields.String(description='a User Name', required=True, example="justkode"),
    'password': fields.String(description='Password', required=True, example="password")
})

# required fields in request body?
jwt_fields = auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'testusr2',
    'password': '1234',
    'database': 'test1',
    'autocommit': True
}

model_config = {
    "username": "testusr2",
    "password": "1234",
    "host": "127.0.0.1",
    "database": "test1",
    "port": 3306,
}


@auth.route('/register')
class AuthRegister(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)
        
    @auth.expect(user_fields)
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={500: 'Register Failed'})
    def post(self):
        """
        Endpoint for registering new users.
        ---
        request body:
        - username: new username
        - password: new password (currently has no length checks etc)
        """

        username = request.json.get('username')
        password = request.json.get('password')


        # using only sql
        # try:
        #     sql, args = "SELECT * FROM User WHERE username=?", (username,)
        #     if len(self.query_db(sql, args=args, retval=True)) != 0:
        #         return {
        #             "message": "User Exists"
        #         }, 200

        #     sql, args = "INSERT INTO User (username, password) VALUES (?, ?)", (username, generate_password_hash(password),)
        #     if self.query_db(sql, args=args):
        #         return {  # return jwt token
        #             "Authorization": "Bearer " + create_access_token(identity={'username': username})
        #         }, 200
            
        # except Exception as e:
        #     return {
        #         "message": "Register Failed",
        #     }, 500


        # using orm model
        try:
            with self.query_model("User") as (conn, User):
                res = conn.execute(select(User).where(User.username == username)).mappings().all()
            
                if len(res) != 0:
                    return {
                        "message": "User Exists"
                    }, 200

                conn.execute(
                    insert(User), {
                        "username": username,
                        "password": generate_password_hash(password),
                    }
                )

                return {
                    "Authorization": "Bearer " + create_access_token(identity={'username': username})
                }, 200

        except Exception as e:
            print(e)
            return {
                "message": "Register Failed",
            }, 500

                
@auth.route('/login')
class AuthLogin(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, model_config=model_config)
        Resource.__init__(self, *args, **kwargs)
        
    @auth.expect(user_fields)
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={200: 'User Not Found'})
    @auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        """
        Endpoint for loging in users
        ---
        req body:
        - username: existing username
        - password: plaintext password
        """
        username = request.json.get('username')
        password = request.json.get('password')

        # using only sql
        # try:
        #     sql, args = "SELECT * FROM User WHERE username=?", (username,)
        #     retval = self.query_db(sql, args=args, retval=True)
        #     if len(retval) == 0:
        #         return {
        #             "message": "User Not Found"
        #         }, 200

        #     user = retval[0]
        #     if not check_password_hash(user[2], password):  # 비밀번호 일치 확인        
        #         return {
        #             "message": "Wrong Password"
        #         }, 200

        #     return {
        #         "Authorization": "Bearer " + create_access_token(identity={'username': username})
        #     }, 200
        
        # except Exception as e:
        #     print(e)
        #     return {
        #         "message": "Login Failed",
        #     }, 500


        # using orm model 
        try:
            with self.query_model("User") as (conn, User):
                parsed = User.validate(data=request.json)
                print(f"{request.json} \n\n {parsed}")
                
                res = conn.execute(select(User).where(User.username == "username")).mappings().all()
                if len(res) == 0:
                    return {
                        "message": "User Not Found"
                    }, 200

                if not check_password_hash(res[0].password, password):
                    return {
                        "message": "Wrong Password"
                    }, 200

                return {
                    "Authorization": "Bearer " + create_access_token(identity={'username': username})
                }, 200

        except Exception as e:
            print(e)
            return {
                "message": "Login Failed",
            }, 500


@auth.route('/get')
class AuthGet(Service, Resource):
    def __init__(self, *args, **kwargs):
        Service.__init__(self, db_config=db_config)
        Resource.__init__(self, *args, **kwargs)
        
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={404: 'Login Failed'})
    def get(self):
        """
        Endpoint for checking if user token is valid.
        ---
        req header
        - Authentication: Bearer [JWT Token]
        """
        if jwt_data := verify_jwt_in_request():
            return jwt_data, 200
        
        return {"message": "unauthenticated"}, 200
        




