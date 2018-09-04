from arrow import Arrow
from datetime import datetime
import arrow


def is_payable(utc: Arrow) -> bool:
    """Should return True if time is 4:20AM or 4:20PM in Texas"""
    central = utc.to('America/Chicago')

    hour = central.hour
    minute = central.minute

    if minute != 20:
        return False

    if hour not in [4, 16]:
        return False

    return True


def strip_date(target_date):
    return arrow.get(datetime(year=target_date.year,
                              month=target_date.month,
                              day=target_date.day,
                              hour=target_date.hour,
                              minute=target_date.minute))
