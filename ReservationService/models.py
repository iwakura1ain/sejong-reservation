from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class _User(BaseModel):
    _id: int = Field(int, title="사용자 unique ID",)
    # userId: int = Field(int, title="사용자 unique ID",)
    # userNum: int = Field(int, title="사용자 학번/직번",)
    name: str = Field(title="사용자 이름",
                      alias="username")
    email: str = Field(title="이메일 @sju.ac.kr or @sejong.ac.kr")
    userType: int = 1
    isAdmin: int = 0
    isBanned: int = 0

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "17010000",
                "email": "honggildong@sju.ac.kr",
                "userType": 1,
                "isAdmin": 0,
                "isBanned": 0,
            }
        }


class _Room(BaseModel):
    _id: int = Field(int, title="회의실 ID",)
    _created: datetime = Field(datetime, title="만들어진 시간",
                               alias="createdAt")
    _updated: datetime = Field(datetime, title="updated 시간",
                               alias="updatedAt")
    name: str = Field(title="회의실 이름",
                      alias="roomName")
    address1: str = Field(None, title="회의실 주소1 (건물이름??)",
                          alias="roomAddress1", )
    address2: str = Field(None, title="회의실 주소2 (층/호수??)",
                          alias="roomAddress2")
    isUsable: int = Field(0, title="회의 가능 여부 0 or 1")
    maxUsers: int = Field(10, title="회의실 최대 수용 인원수 (임의 기본값=10)")
    previewimage: list | None = None

    class Config:
        orm_mode = True


class _Reservation(BaseModel):
    id: Optional[int] = Field(None, title="예약 ID")
    # alias="reservationId")
    _created: Optional[datetime] = Field(datetime, title="만들어진 시간",
                               alias="createdAt")
    _updated: Optional[datetime] = Field(datetime, title="마지막 변경 시간",
                               alias="updatedAt")
    reservationTopic: str = Field(..., title="회의 내용",
                                  alias="reservationTopic")
    reservationDate: date = Field(..., title="회의실 예약일",
                                  alias="reservationDate")
    reservationType: int = Field(1, title="예약 타입")
    roomID: int = Field(None, title="예약한 회의실 ID",
                        alias="reservationRoom")
    creatorID: int = Field(None, title="예약한 회의실 ID",
                           alias="creator")
    # members: None = None
    roomUsed: Optional[bool] | None = None
    roomInfo: Optional[_Room] = Field(None, title="회의실 정보")
    creatorInfo: Optional[_User] = Field(None, title="예약자 정보")

    class Config:
        orm_mode = True

        schema_exclude = ["id"]