from os import getenv

# model_config = {
#   "username": "development",
#   "password": "1234",
#   "host": "sejong-reservation-dbservice-1",
#   "port": 3306,
# }

model_config = {
    "username": getenv("DB_USERNAME"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_URL"),
    "port": getenv("DB_PORT"),
    "database": getenv("DB_NAME")
}

api_config = {
  "get_auth_info": "http://userservice:5000/auth/jwt-status",
  "get_rooms_info": "http://adminservice:5000/admin/rooms",
}
