# import jwt
# from jwt.exceptions import DecodeError

from flask import g, request
from flask_restx import Resource, fields, Namespace, Api
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
)

from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, get_cur



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


@auth.route('/register')
class AuthRegister(Resource):
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

        db = get_db()
        cur = get_cur()

        try:  # check if user exists in db
            cur.execute(
                "SELECT * FROM User WHERE username=?",
                (username,),
            )
            if cur.fetchone() is not None:  # when user exists
                return {
                    "message": "User Exists"
                }, 200
        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        try:  # add user into db
            cur.execute(
                "INSERT INTO User (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        return {  # return jwt token
            "Authorization": "Bearer " + create_access_token(
                identity={'username': username}
            )
        }, 200


@auth.route('/login')
class AuthLogin(Resource):
    @auth.expect(user_fields)
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={404: 'User Not Found'})
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

        db = get_db()
        cur = get_cur()
        
        try:  # check if user exists in db
            cur.execute(
                "SELECT * FROM User WHERE username=?",
                (username,),
            )
    
            user = cur.fetchone()
            if user is None:
                return {
                    "message": "User Not Found"
                }, 404
            
        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        try:  # check password hash
            if not check_password_hash(user[2], password):  # 비밀번호 일치 확인        
                return {
                    "message": "Auth Failed"
                }, 500

        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        return {
            "Authorization": "Bearer " + create_access_token(identity={'username': username})
        }, 200


@auth.route('/get')
class AuthGet(Resource):
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
        




