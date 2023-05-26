from sqlalchemy import select, update, and_
from service import Service

from datetime import date, time, datetime

from config import model_config, api_config

def check_room_used(room_id, service=None):
    try:
        with service.query_model("Reservation") as (conn, Reservation):
            now_date = datetime.now().date()
            now_time = datetime.now().time()

            stmt = (select(Reservation)
                # select for a room
                .where(Reservation.room_id == room_id)
                # for today
                .where(Reservation.reservation_date == now_date)
                # only reservations from the past
                .where(Reservation.end_time < now_time)
                # room not used
                .where(Reservation.room_used == 0)
            )
            rows = conn.execute(stmt).mappings().fetchall()

            no_show_users = []
            for row in rows:
                if row["room_used"] == 0:
                    no_show_users.append(row["creator_id"])
            
        # TODO: maybe use query_api?
        with service.query_model("User") as (conn, User):
            for user_id in no_show_users:
                stmt = (
                    update(User)
                    .where(User.id == user_id)
                    .values(no_show=User.no_show+1)
                )
                conn.execute(stmt)

                # # sanity check
                # row = conn.execute(select(User).where(User.id == user_id))
                # print(row.mappings().fetchone())
        return True

    except Exception:
        return False

if __name__ == "__main__":
    model_config = {
        "username": "development",
        "password": "1234",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "sejong"
    }

    service = Service(model_config=model_config,
                      api_config=api_config)

    room_ids = [1,2,3]
    for id in room_ids:
        check_room_used(id,service=service)
