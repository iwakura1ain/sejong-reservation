from os import getenv

# raw sql config
# SQL = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'testusr2',
#     'password': '1234',
#     'database': 'test1',
#     'autocommit': True
# }

#orm config
ORM = {
    "username": getenv("DB_USERNAME"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_URL"),
    "port": getenv("DB_PORT"),
    "database": getenv("DB_NAME")
}


# # local orm config
# ORM = {
#     "username": "development",
#     "password": "1234",
#     "host": "127.0.0.1",
#     "port": 3306,
#     "database": "sejong"
# }

api_config = {
    "send_email": "http://alertservice:5003/alert",
}

# email address from which alert emails will be sent
SENDER = "ernie937@gmail.com"

# 학과 정보
dept_str = {
    1: "컴퓨터공학과",
    2: "기타 학과",
}

# 사용자 구분 정보
user_type_str = {
    1: "관리자",
    2: "교수",
    3: "대학원생",
    4: "학부생",
}
