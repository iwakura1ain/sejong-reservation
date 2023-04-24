from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select, insert, update, delete

from classy_fastapi import Routable
from classy_fastapi import get as classy_get

from service import Service
from models import _Room
from config import db_config, model_config

class RoomRoutes(Routable):
    def __init__(self, model_config, db_config) -> None:
        super().__init__()
        self.__service = Service(
            model_config=model_config,
            db_config=db_config)
    
    @classy_get(path="/{id}",description="")
    def get_room_by_id(self, id:int|None=None):
        """
        - GET /room/1
        """
        try:
            with self.__service.query_model("Room") as (conn,Room):
                if id:
                    stmt = select(Room).where(Room.id == id)
                    rows = conn.execute(stmt).all()
                    rows = _Room.from_orm(rows[0])
                else: 
                    stmt = select(Room)
                    rows = conn.execute(stmt).all()
                    rows = [_Room.from_orm(row) for row in rows]
                return rows
        except Exception as e:
            return JSONResponse({"message":str(e)}, 200)
