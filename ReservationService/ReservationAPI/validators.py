from service import validator
from datetime import date, time

@validator("Reservation.start_time","Reservation.end_time")
def validate_time(start_time, end_time):
    """
    checks validity of reservation's start_time and end_time 
    - start_time should be earlier than end_time.
    - reservation should be within open hours.
    """
    # check if time values are passed in with proper formattng
    try:
        start_time = time(start_time)
        end_time = time(end_time)
    except Exception as e:
        return False
    if start_time > end_time:
        return False
    return True

@validator("Reservation.reservation_topic")
def validate_reservation_topic(reservation_topic):
    """
    reservation_topic string len check
    """
    if len(reservation_topic) > 100:
        return False
    return True
