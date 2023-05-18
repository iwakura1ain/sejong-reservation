from os import getenv
from datetime import timedelta

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

reservation_limit = {
    1: timedelta.max,
    2: timedelta.max,
    3: timedelta(weeks=1),
    4: timedelta(days=2)
}
