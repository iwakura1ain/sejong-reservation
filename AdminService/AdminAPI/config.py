from os import getenv

# model configuration for orm model
model_config = {
    # "username": getenv("DB_USERNAME"),
    # "password": getenv("DB_PASSWORD"),
    # "host": getenv("DB_URL"),
    # "port": getenv("DB_PORT"),
    # "database": getenv("DB_NAME")
    
    # local setting
    "host": "127.0.0.1",
    "database": "sejong",
    "port": 3306,
    "username": "development",
    "password": 1234
}

api_config = {
    "jwt_status": "http://127.0.0.1:5001/auth/jwt-status",
}

filepath = "/Users/chow/Documents/GitHub/sejong-reservation/AdminService/AdminAPI/static"