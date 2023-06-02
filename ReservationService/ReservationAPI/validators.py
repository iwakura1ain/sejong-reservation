from datetime import date, time, datetime

from service import validator


@validator("Reservation.reservation_date", "Reservation.start_time")
def validate_time(reservation_date, start_time):
    """
    This function validates the start time of a reservation by checking if it is valid and not in the
    past.
    
    :param reservation_date: The date of the reservation in ISO format (YYYY-MM-DD)
    :param start_time: The start time of a reservation. It is a string in the format "HH:MM:SS"
    (hours:minutes:seconds)
    :return: a boolean value indicating whether the reservation's start time is valid or not. True is
    returned if the start time is valid, and False is returned if it is not valid.
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
    """
    This Python function validates if a reservation end time is valid and not in the past.
    
    :param reservation_date: The date of the reservation in ISO format (YYYY-MM-DD)
    :param end_time: The end time of a reservation, represented as a string in the format "HH:MM"
    :return: a boolean value. It returns True if the reservation date and end time are valid and not in
    the past, and False otherwise.
    """
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
    This function validates the start and end times of a reservation by checking if the start time is
    earlier than the end time.
    
    :param reservation_date: The date of the reservation in ISO format (YYYY-MM-DD)
    :param start_time: The start time of a reservation, in the format of "HH:MM:SS" (hours, minutes,
    seconds)
    :param end_time: The end time of a reservation
    :return: a boolean value indicating whether the reservation's start_time is earlier than its
    end_time.
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


