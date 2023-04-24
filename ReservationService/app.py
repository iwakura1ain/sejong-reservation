from fastapi import FastAPI

import reservation, rooms, users, config

app = FastAPI()

app.include_router(reservation.router)
app.include_router(users.router)
# app.include_router(rooms.router)
room_routes = rooms.RoomRoutes(db_config=config.db_config,
                               model_config=config.model_config)
app.include_router(room_routes.router,
                   prefix="/room", tags=["room"])


@app.get("/")
def hello():
    return "hello from Reservation"
