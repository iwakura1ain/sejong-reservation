from fastapi import FastAPI

import orm
import reservation

app = FastAPI()

@app.get("/")
def hello():
    return "hello from Reservation"

app.include_router(orm.router)
app.include_router(reservation.router)
