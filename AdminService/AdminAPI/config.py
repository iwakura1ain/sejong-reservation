from os import getenv

# model configuration for orm model
model_config = {
    "username": getenv("DB_USERNAME"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_URL"),
    "port": getenv("DB_PORT"),
    "database": getenv("DB_NAME"),

    # "username": "development",
    # "password": 1234,
    # "host": "dbservice",
    # "port": 3306,
    # "database": "sejong"
}

api_config = {
    "jwt_status": "http://userservice:5000/auth/jwt-status",
}

filepath = "/tmp"
