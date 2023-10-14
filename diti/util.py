from datetime import datetime as dt
from typing import Union
import pytz

def timezone_to_offset_str(timezone: pytz.tzinfo.BaseTzInfo, datetime: dt) -> str:
    newdt = dt.fromtimestamp(datetime.timestamp())
    offset_mins = int(timezone.utcoffset(newdt).total_seconds() // 60)
    offset_str = "{:+03d}:{:02d}".format(offset_mins // 60, offset_mins % 60)
    return offset_str


def offset_str_to_minutes(offset_str) -> int:
    dt.strptime(offset_str, "%z")
    multiplier = 1 if offset_str[0] == "+" else -1
    offset_hours = int(offset_str[1:3])
    offset_minutes = int(offset_str[4:])
    total_offset_minutes = (offset_hours * 60 + offset_minutes) * multiplier
    return total_offset_minutes


def parse_timezone(
    timezone: Union[str, int, None]
) -> pytz.tzinfo.BaseTzInfo:
    __tz = None
    if isinstance(timezone, str):
        if timezone.startswith("+") or timezone.startswith("-"):
            offset = offset_str_to_minutes(timezone)
            __tz = pytz.FixedOffset(offset)
        else:
            __tz = pytz.timezone(timezone)
    elif isinstance(timezone, int):
        offset = timezone
        __tz = pytz.FixedOffset(offset)
    else:
        __tz = pytz.timezone("UTC")
    return __tz


def parse_date_time(date_time: Union[dt, int, float, str, None]) -> dt:
    __dt = None
    if isinstance(date_time, dt):
        __dt = date_time
    elif isinstance(date_time, int) or isinstance(date_time, float):
        __dt = dt.fromtimestamp(date_time, tz=pytz.UTC)
    elif isinstance(date_time, str):
        __dt = dt.fromisoformat(date_time)
    else:
        __dt = dt.now()

    return __dt


def get_daycount_of_month(month: int, year: int):
    day_count = 31
    if month in [4, 6, 9, 11]:
        day_count = 30
    elif month == 2:
        day_count = (
            29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        )
    return day_count
