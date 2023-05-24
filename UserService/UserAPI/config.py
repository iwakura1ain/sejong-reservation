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
