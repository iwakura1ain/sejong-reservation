from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from sqlalchemy import select, insert, update, delete

from service import Service
from models import _Reservation, _User, _Room
from config import db_config, model_config
import requests

# include = {"reservationDate", "reservationTopic", "roomID", "creatorID"}
exclude = {"creatorInfo","roomInfo"}

# TODO: look for better alternatives than fastapi.Depends
service = None


def get_service():
    global service
    service = Service(model_config=model_config)
    yield
    service = None


router = APIRouter(
    prefix="/reservation",
    dependencies=[Depends(get_service)],
    tags=["reservation"],
)


@router.get("",
            description="예약 조회",
            status_code=status.HTTP_200_OK,
            )
def get_reservation(# id: int|None = None,
    # TODO:filter by y,ym,ymd,md
    ):
    try:
        with service.query_model("Reservation") as (conn, Reservation):
            stmt = select(Reservation)
            rows = conn.execute(stmt).all()
            rows = [_Reservation.from_orm(row) for row in rows]
        print(rows)

        # if no rows to return
        if not rows:
            return Response({"message":"No content"}, status_code=status.HTTP_204_NO_CONTENT)

        for row in rows:
            # get roomInfo for each reservation
            # TODO: replace with service.query_api
            r = requests.get( 
                f"http://localhost:5555/room/{row.roomID}").json()
            row.roomInfo = _Room(**r)
            # TODO: get creatorInfo for each reservation

        # if no rows to return
        if not rows:
            return Response({"message":"Wrong ID"}, status.HTTP_200_OK)
        # else return rows
        return rows

    except Exception as e:
        return JSONResponse({"message": str(e)}, status.HTTP_200_OK)


@router.get("/{id}",
            description="예약 조회 by id")
def get_reservation_by_id(id:int=None):
    """
    - GET /reservation/15
    """
    try:
        with service.query_model("Reservation") as (conn, Reservation):
            # if no id, return 204 no content
            if not id:
                return Response({"message":"No Contnet"},status.HTTP_204_NO_CONTENT)
            # if id has value, select only for that id
            stmt = select(Reservation).where(Reservation.id == id)
            rows = conn.execute(stmt).all()
            row = _Reservation.from_orm(rows[0])
            # get roomInfo,creatorInfo for each reservation
            # TODO: replace with service.query_api
            r = requests.get( 
                f"http://localhost:5555/room/{row.roomID}").json()
            row.roomInfo = _Room(**r)
            return row.dict(exclude_unset=True)
    except IndexError as e:
        return JSONResponse({"message": "No Content"}, status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"message": str(e)}, status.HTTP_200_OK)


@router.post("",
             description="예약 추가",
            #  status_code=status.HTTP_201_CREATED,
             )
def create_reservation(reservation: _Reservation):
    """
    - POST /reservation
    """
    try:
        # TODO: fix unconsumed column names
        with service.query_model("Reservation") as (conn, Reservation):
            stmt = (insert(Reservation)
                    .values(reservation.dict()))
            res = conn.execute(stmt).all()
            # if res returns no rows, then return 201 with reservation
            # return JSONResponse({"message":"created"})

    except Exception as e:
        return JSONResponse({"message": str(e)})


@router.patch("/{id}",
              description="예약 변경")
def update_reservation_by_id(id: int, reservation: _Reservation):
    """
    - PATCH /reservation/15 -d {...}
    """
    # TODO: finish implementing patch update 
    # docs: https://fastapi.tiangolo.com/tutorial/body-updates/#body-updates
    try:
        with service.query_model("Reservation") as (conn, Reservation):
            stmt = select(Reservation).where(Reservation.id == id)
            res = conn.execute(stmt).all()
            original_reservation = _Reservation.from_orm(res[0])
            assert type(original_reservation) == _Reservation
            print(original_reservation.id, original_reservation)

            update_data = reservation.dict(exclude_unset=True)
            assert type(update_data) == dict
            print(update_data)
            updated_model = original_reservation.copy(update=update_data)
            assert type(updated_model) == _Reservation
            print(updated_model._id)

            stmt = (update(Reservation)
                    .where(Reservation.id == updated_model._id)
                    .values(jsonable_encoder(updated_model, exclude=exclude)))
            res = conn.execute(stmt)

            # if res returns no rows, then return 200 with reservation
            if not res.returns_rows:
                return JSONResponse(
                    {"result": str((res,updated_model))}, 200)
    except ValidationError as e:
        return JSONResponse({"message": "모든 정보가 제대로 주어졌는지 확인"}, 200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, 200)


@router.delete("/{id}",
               description="예약 삭제")
def delete_reservation(id: int):
    """
    - DELETE /reservation/10
    """
    try:
        with service.query_model("Reservation") as (conn, Reservation):
            stmt = delete(Reservation).where(Reservation.id == id)
            res = conn.execute(stmt)
            return JSONResponse({"result": str(res)}, 200)
    except Exception as e:
        return JSONResponse({"message": str(e)}, 200)
