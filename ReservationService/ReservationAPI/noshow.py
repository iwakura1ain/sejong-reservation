from sqlalchemy import select, update, and_
from service import Service

from datetime import date, time, datetime

from config import model_config, api_config


class NoShowCheck(Service):
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from Service
        class, passing arguments to their respective initialization functions.
        """
        Service.__init__(
            self, model_config=model_config, api_config=api_config
        )

    def check_noshow(self):
        noshow_counts = self.get_noshow()
        for creator, count in noshow_counts.items():
            print("incrementing: ", creator, count, flush=True)
            res = self.increment_noshow(creator, count)
            print(res)

    
    def increment_noshow(self, creator, count):
        try:
            res = self.query_api(
                "increment_noshow", "post",
                request_params={"user_id": creator},
                body={"noshow_count": count}
            )
            return res.get("status")

        except Exception:
            return False

    def get_noshow(self):
        try:
            with self.query_model("Reservation") as (conn, Reservation):
                now_date = datetime.now().date()
                now_time = datetime.now().time()

                stmt = (
                    select(Reservation)
                    # for today
                    .where(Reservation.reservation_date == now_date)
                    # only reservations from the past
                    .where(Reservation.end_time < now_time)
                    # room not used
                    .where(Reservation.room_used == 0)
                )
                rows = conn.execute(stmt).mappings().fetchall()

            noshow_counts = {}
            for r in rows:
                creator = r["creator_id"]
                if creator in noshow_counts.keys():
                    noshow_counts[creator] += 1
                else:
                    noshow_counts[creator] = 1

            return noshow_counts

        except Exception:
            return {}


no_show_check = NoShowCheck()
if __name__ == "__main__":
    no_show_check.check_noshow()
