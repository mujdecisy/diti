from enum import Enum
import pytz
from typing import Union
from datetime import datetime as dt, timedelta as td
from dateutil.relativedelta import relativedelta as rtd


class FormatEnum(Enum):
    FMT_MIL_TZ: str = "%Y-%m-%dT%H:%M:%S.%f%z"
    FMT_MIL: str = "%Y-%m-%dT%H:%M:%S.%f"
    FMT_SEC_TZ: str = "%Y-%m-%dT%H:%M:%S%z"
    FMT_SEC: str = "%Y-%m-%dT%H:%M:%S"
    FMT_MIN_TZ: str = "%Y-%m-%dT%H:%M%z"
    FMT_MIN: str = "%Y-%m-%dT%H:%M"
    FMT_HOU_TZ: str = "%Y-%m-%dT%H%z"
    FMT_HOU: str = "%Y-%m-%dT%H"
    FMT_DAY_TZ: str = "%Y-%m-%d%z"
    FMT_DAY: str = "%Y-%m-%d"
    FMT_MON_TZ: str = "%Y-%m%z"
    FMT_MON: str = "%Y-%m"
    FMT_YEA_TZ: str = "%Y%z"
    FMT_YEA: str = "%Y"


class PartEnum(Enum):
    YEAR = 0
    MONTH = 1
    WEEK = 2
    DAY = 3
    HOUR = 4
    MINUTE = 5
    SECOND = 6
    MICROSECOND = 7


PART_FORMAT = {
    PartEnum.YEAR: "%Y",
    PartEnum.MONTH: "%m",
    PartEnum.WEEK: "%W",
    PartEnum.DAY: "%d",
    PartEnum.HOUR: "%H",
    PartEnum.MINUTE: "%M",
    PartEnum.SECOND: "%S",
    PartEnum.MICROSECOND: "%f",
}

PART_DELTA = {
    PartEnum.YEAR: lambda x: rtd(years=x),
    PartEnum.MONTH: lambda x: rtd(months=x),
    PartEnum.WEEK: lambda x: rtd(weeks=x),
    PartEnum.DAY: lambda x: td(days=x),
    PartEnum.HOUR: lambda x: td(hours=x),
    PartEnum.MINUTE: lambda x: td(minutes=x),
    PartEnum.SECOND: lambda x: td(seconds=x),
    PartEnum.MICROSECOND: lambda x: td(microseconds=x),
}


def timezone_to_offset_str(timezone: pytz.tzinfo.BaseTzInfo) -> str:
    offset_mins = int(timezone.utcoffset(None).total_seconds() // 60)
    offset_str = "{:+03d}{:02d}".format(offset_mins // 60, offset_mins % 60)
    return offset_str


def offset_str_to_minutes(offset_str) -> int:
    dt.strptime(offset_str, "%z")
    multiplier = 1 if offset_str[0] == "+" else -1
    offset_hours = int(offset_str[1:3])
    offset_minutes = int(offset_str[3:])
    total_offset_minutes = (offset_hours * 60 + offset_minutes) * multiplier
    return total_offset_minutes


def parse_timezone(timezone: Union[str, int, None]) -> pytz.tzinfo.BaseTzInfo:
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
        __dt = None
        for fmt in FormatEnum:
            try:
                __dt = dt.strptime(date_time, fmt.value)
            except ValueError:
                continue
        if __dt == None:
            raise ValueError("[date_time] string parameter does not match any format")
    else:
        __dt = dt.now()

    return __dt


def get_daycount_of_month(month: int, year: int):
    day_count = 31
    if month in [4, 6, 9, 11]:
        day_count = 30
    elif month == 2:
        day_count = 29 if year % 4 == 0 else 28
    return day_count
