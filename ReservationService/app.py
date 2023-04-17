from fastapi import FastAPI, APIRouter
from fastapi import Response, HTTPException
from fastapi.responses import JSONResponse

import orm

app = FastAPI()

@app.get("/")
def hello():
    return "hello from Reservation"

@app.get("/orm")
def hello_orm():
    myorm = orm.sampleORM()
    # sqlalchemy objects are NOT compatible with JSONResponse
    return str(myorm.tables['User']) 

reservation = APIRouter(prefix="/reservation")

@reservation.get("")
def get_reservation():
    reservations = []

    # append sample data
    x = {
        "reservationID": 12121,
        "reservationDate": "2023-04-20",
        "reservatioTimeslot": [10,11,12,13],
        "reservationTopic": "회의실 예약시스템 API설계 회의",
        "creatorId": 17011540,
        "reservationRoomID":1
    }
    reservations.append(x)

    print(reservations)
    # get data

    # return reservations
    return JSONResponse(
        content={"result":True,"message":"",
        "reservations":reservations},
        status_code=200)


    







app.include_router(reservation)
