import jwt
import bcrypt
from flask import request
from flask_restx import Resource, Api, Namespace, fields

users = {}

Auth = Namespace(
    name="Auth",
    description="사용자 인증을 위한 API",
)

user_fields = Auth.model('User', {  # Model 객체 생성
    'name': fields.String(description='a User Name', required=True, example="justkode")
})

user_fields_auth = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = Auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})


@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={500: 'Register Failed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        if name in users:
            return {
                "message": "Register Failed"
            }, 500
        
        else:
            users[name] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())  # 비밀번호 저장
            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256")  # str으로 반환하여 return
            }, 200
        
        
@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth)
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'User Not Found'})
    @Auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        name = request.json['name']
        password = request.json['password']
        if name not in users:
            return {
                "message": "User Not Found"
            }, 404

        elif not bcrypt.checkpw(password.encode('utf-8'), users[name]):  # 비밀번호 일치 확인
            return {
                "message": "Auth Failed"
            }, 500

        else:
            return {
                'Authorization': jwt.encode({'name': name}, "secret", algorithm="HS256") # str으로 반환하여 return
            }, 200
        
        
@Auth.route('/get')
class AuthGet(Resource):
    @Auth.doc(responses={200: 'Success'})
    @Auth.doc(responses={404: 'Login Failed'})
    def get(self):
        header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        if header == None:
            return {"message": "Please Login"}, 404
        data = jwt.decode(header, "secret", algorithms="HS256")
        return data, 200
