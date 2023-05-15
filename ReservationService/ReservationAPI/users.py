from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from service import Service
from models import _Room
from config import db_config, model_config
from typing import Optional

service =  None
def get_service():
    global service
    service =  Service(model_config=model_config)
    yield
    service =  None

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_service)],
)

@router.get(path="",
    description="사용자 조회 by id")
def get_user_by_id(id:int|None=None):
    """
    - GET /user/1
    """
    try:
        with service.query_model("Users") as (conn,User):
            if id:
                stmt = select(User).where(User.id==id)
            else: 
                stmt = select(User)
            rows = conn.execute(stmt).all()
            ret = [_Room.from_orm(row) for row in rows]
            # JSONResponse로 묶지말고 
            # pydantic type그대로 리턴하면 
            # fastapi가 스마트하게 잘 jsonify해줌
            return ret
    except Exception as e:
        return JSONResponse({"message":str(e)}, 200)