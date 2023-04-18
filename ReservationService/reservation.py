from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse

from sqlalchemy import insert
from sqlalchemy.orm import Session
import orm

router = APIRouter(prefix="/reservation")

@router.get("")
def get_all_reservations(myorm=Depends(orm.get_orm)):
    reservations = []
    table = myorm.tables["Reservation"]
    with Session(myorm.engine) as session:
        reservations = session.execute(table.select()).all()
        reservations = [str(x) for x in reservations]
        # row = session.execute(select(table)).first()
        # reservations.append(str(row)) 
    # todo: parsing from sqlalchemy object
    return reservations

# class Reservation:
#     __table__ = sampleORM.tables["Reservation"]

def iinsert(myorm):
    Reservation = myorm.tables["Reservation"]

    # Reservation.c.
    # new_reservation = Reservation(
    #     reservationTopic="회의실 예약시스템 API설계 회의",
    #     reservationDate="2023-04-20",
    #     creatorId=17011540,
    #     roomUsed=1,
    # )
    # todo: timeslots

    session = Session(myorm.engine)
    with myorm.engine.connect() as conn:
        #### #1
        # stmt = insert(Reservation) \
        #         .values(
        #             reservationTopic="회의실 예약시스템 API설계 회의",
        #             reservationRoom=1,
        #             reservationType=1,
        #             creator=1,
        #             members=str([])
        #             )
        # result = conn.execute(stmt)
        # conn.commit()
        #### #2
        result = conn.execute(
            insert(Reservation),
            [
                {
                    "reservationTopic":"meeting3",
                    "reservationDate":"2023-04-23",
                    "reservationRoom":1,
                    "reservationType":1,
                    "creator":1,
                    "members":str([])
                }
            ]
        )
        conn.commit()
        conn.close()
    return result


@router.post("")
def make_a_reservation(myorm=Depends(orm.get_orm)):
    try:
        res = iinsert(myorm)
        return JSONResponse({"message":"",
                        "result":str(res)}, 200)
    except Exception as e:
        return JSONResponse({"message":str(e)}, 200)
