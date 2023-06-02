from sqlalchemy import select, update, and_
from service import Service

from datetime import date, time, datetime

from config import model_config, api_config



model_config_cron = {
    "username": "development",
    "password": "1234",
    "host": "dbservice",
    "port": 3306,
    "database": "sejong"
}

api_config_cron = {
    # docker config
    "get_auth_info": "http://userservice:5000/auth/jwt-status",
    "increment_noshow": "http://userservice:5000/users/{user_id}/no-show",
    "get_rooms_info": "http://managementservice:5000/admin/rooms/{id}",
    "send_email": "http://alertservice:5000/alert",
}


# The NoShowCheck class is a subclass of Service that checks for no-show reservations and updates the
# no-show count for each creator.
class NoShowCheck(Service):
    def __init__(self, *args, **kwargs):
        """
        This is the initialization function for a class that inherits from Service
        class, passing arguments to their respective initialization functions.
        """
        Service.__init__(
            self, model_config=model_config_cron, api_config=api_config_cron
        )

    def check_noshow(self):
        """
        This function checks the number of no-shows for each creator and increments their count
        accordingly.
        """
        noshow_counts = self.get_noshow()
        for creator, count in noshow_counts.items():
            res = self.increment_noshow(creator, count)
    
    def increment_noshow(self, creator, count):
        """
        This function increments the noshow count for a given user and returns the status of the
        operation.
        
        :param creator: The creator parameter is the user ID of the creator whose noshow count needs to
        be incremented
        :param count: The count parameter is an integer value representing the number of no-shows to be
        incremented for a particular user
        :return: either the value of `res.get("status")` or `False`.
        """
        import json

        try:
            headers = {'Content-type': 'application/json', 'Accept': '*/*'}
            body = json.dumps({"noshow_count": int(count)})
            
            res = self.query_api(
                "increment_noshow", "post",
                request_params={"user_id": creator},
                headers=headers,
                body=body
            )
            return res.get("status")

        except Exception:
            return False

    def get_noshow(self):
        """
        This function retrieves unused reservations for the current day and updates the room_used field
        to -1, while also keeping track of the number of no-shows for each reservation creator.
        :return: a dictionary containing the number of no-shows for each reservation creator. If an
        exception occurs, an empty dictionary is returned.
        """
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
                unused_reservations = []
                for r in rows:
                    creator = r["creator_id"]
                    if creator in noshow_counts.keys():
                        noshow_counts[creator] += 1
                    else:
                        noshow_counts[creator] = 1

                    conn.execute(
                        update(Reservation)
                        .where(Reservation.id == r["id"])
                        .values(room_used=-1)
                    )

                print(f"updating noshow counts for {noshow_counts}")
                
            return noshow_counts

        except Exception:
            return {}


no_show_check = NoShowCheck()
if __name__ == "__main__":
    print("=================running cronjob=====================", flush=True)
    no_show_check.check_noshow()

