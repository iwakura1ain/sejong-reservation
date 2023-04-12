# import jwt
# from jwt.exceptions import DecodeError

from flask import (
    flash, g, request, session, url_for
)

from flask_restx import Resource, fields, Namespace, Api

from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request, JWTManager
)

from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, get_cur



auth = Namespace(
    name="auth",
    description="사용자 인증을 위한 API",
)


user_fields = auth.model('User', {  # Model 객체 생성
    'username': fields.String(description='a User Name', required=True, example="justkode"),
    'password': fields.String(description='Password', required=True, example="password")
})

jwt_fields = auth.model('JWT', {
    'Authorization': fields.String(description='Authorization which you must inclued in header', required=True, example="eyJ0e~~~~~~~~~")
})


@auth.route('/register')
class AuthRegister(Resource):
    @auth.expect(user_fields)
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={500: 'Register Failed'})
    def post(self):
        username = request.json['username']
        password = request.json['password']
        print(f"received {username}|{password}")

        db = get_db()
        cur = get_cur()

        try:
            cur.execute(
                "SELECT * FROM User WHERE username=?",
                (username,),
            )
            if cur.fetchone() is not None:
                return {
                    "message": "User Exists"
                }, 200
        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        try:
            cur.execute(
                "INSERT INTO User (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500

        return {
            #'Authorization': jwt.encode({'username': username}, "secret", algorithm="HS256")  # str으로 반환하여 return
            "Authorization": create_access_token(identity={'username': username})
        }, 200


@auth.route('/login')
class AuthLogin(Resource):
    @auth.expect(user_fields)
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={404: 'User Not Found'})
    @auth.doc(responses={500: 'Auth Failed'})
    def post(self):
        username = request.json['username']
        password = request.json['password']
        print(f"received {username}|{password}")

        db = get_db()
        cur = get_cur()
        
        try:
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

        try:
            if check_password_hash(user[2], password):  # 비밀번호 일치 확인
                return {
                    #'Authorization': jwt.encode({'username': username}, "secret", algorithm="HS256") # str으로 반환하여 return
                    "Authorization": create_access_token(identity={'username': username})
                }, 200
                
            return {
                "message": "Auth Failed"
            }, 500

            # session.clear()
            # session['user_id'] = user[0]
            # print(f"user {username} logged in")  

        except Exception as e:
            return {
                "message": "Register Failed",
                "error": e
            }, 500


@auth.route('/get')
class AuthGet(Resource):
    @auth.doc(responses={200: 'Success'})
    @auth.doc(responses={404: 'Login Failed'})
    def get(self):
        #try:
        if jwt_data := verify_jwt_in_request() is not None:
            print(jwt_data)
            return jwt_data, 200
        
        return {"message": "unauthenticated"}, 200
        

        # except DecodeError:
        #     return {"message": "unauthenticated"}, 200

        # header = request.headers.get('Authorization')  # Authorization 헤더로 담음
        # if header is None:
        #     return {"message": "Please Login"}, 404

        # try:
        #     data = jwt.decode(header, "secret", algorithms="HS256")
        #     return data, 200
    
        # except DecodeError:
        #     return {"message": "unauthenticated"}, 200


# @AUTH.route('/logout')
# def logout():
#     def get(self):
#         session.clear()
#         return redirect(url_for('index'))


# #@Auth.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         db = get_db()
#         cur = get_cur()
#         cur.execute(
#             'SELECT * FROM User WHERE id = ?', (user_id,)
#         )
#         g.user = cur.fetchone()


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view


    
# ==================================================

# import functools
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import *


# bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         print(f"got from frontend: {username} | {password}")

#         db = get_db()
#         cur = get_cur()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 cur.execute(
#                     "INSERT INTO User (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 #db.commit()
#             except Exception as e:
#                 error = e
#             else:
#                 return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template('register.html')


# @bp.route('/login', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         print(f"username|password: {username}|{password}")

#         db = get_db()
#         cur = get_cur()

#         error = None
#         cur.execute(
#             "SELECT * FROM User WHERE username = ?", (username,)
#         )
#         user = cur.fetchone()


#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user[2], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user[0]
#             return redirect(url_for('index'))

#         flash(error)
#         print(f"user {username} logged in")   

#     return render_template('login.html')


# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         cur = get_cur()
#         cur.execute(
#             'SELECT * FROM User WHERE id = ?', (user_id,)
#         )
#         g.user = cur.fetchone()


# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view




