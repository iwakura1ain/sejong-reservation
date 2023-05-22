from os import getenv

# model configuration for orm model
model_config = {
    "username": getenv("DB_USERNAME"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_URL"),
    "port": getenv("DB_PORT"),
    "database": getenv("DB_NAME"),

    # local setting
    # "username": "development",
    # "password": 1234,
    # "host": "127.0.0.1",
    # "port": 3306,
    # "database": "sejong"
}

api_config = {
    "jwt_status": "http://userservice:5000/auth/jwt-status",
}

filepath = "/Users/chow/Documents/GitHub/sejong-reservation/AdminService/AdminAPI/static"