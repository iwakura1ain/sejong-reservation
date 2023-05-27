from datetime import date, time, datetime

from service import validator


@validator("Reservation.reservation_date", "Reservation.start_time")
def validate_time(reservation_date, start_time):
    """
    checks validity of reservation's start_time and end_time 
    - start_time should be earlier than end_time.
    """
    try:
        start_dt = datetime.combine(
            date.fromisoformat(reservation_date),
            time.fromisoformat(start_time)
        )
    except Exception:
        return False

    # if trying to make reservation behind now, return false
    if start_dt < datetime.now():
        return False

    return True


@validator("Reservation.reservation_date", "Reservation.end_time")
def validate_time(reservation_date, end_time):
    try:
        end_dt = datetime.combine(
            date.fromisoformat(reservation_date),
            time.fromisoformat(end_time)
        )
    except ValueError:
        return False

    # if trying to make reservation behind now, return false
    if end_dt < datetime.now():
        return False

    return True


@validator("Reservation.reservation_date", "Reservation.start_time", "Reservation.end_time")
def validate_time(reservation_date, start_time, end_time):
    """
    checks validity of reservation's start_time and end_time 
    - start_time should be earlier than end_time.
    """
    try:
        start_dt = datetime.combine(
            date.fromisoformat(reservation_date),
            time.fromisoformat(start_time)
        )
        end_dt = datetime.combine(
            date.fromisoformat(reservation_date),
            time.fromisoformat(end_time)
        )
    except ValueError:
        return False

    # if start_time is ahead of end_time, return false
    if start_dt >= end_dt:
        return False

    return True


