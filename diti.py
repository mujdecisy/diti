import pytz
from typing import Union
from datetime import datetime as dt
from diffcalc import PART_DIFF_CALC

from util import (
    PART_DELTA,
    PART_FORMAT,
    FormatEnum,
    PartEnum,
    offset_str_to_minutes,
    parse_date_time,
    parse_timezone,
    timezone_to_offset_str,
)


class MutableDatetime:
    def __init__(self, datetime: dt | None = None):
        if datetime == None:
            datetime = dt.now()
        self.update(datetime)

    def update(self, datetime: dt) -> None:
        self.year = datetime.year
        self.month = datetime.month
        self.day = datetime.day
        self.hour = datetime.hour
        self.minute = datetime.minute
        self.second = datetime.second
        self.microsecond = datetime.microsecond
        self.tzinfo = datetime.tzinfo

    def to_dt(self) -> dt:
        return dt(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            self.tzinfo,
        )


class Diti:
    _mdt: MutableDatetime
    _tz: pytz.tzinfo.BaseTzInfo

    def __init__(
        self,
        date_time: Union[dt, int, float, str, MutableDatetime, None] = None,
        timezone: Union[str, int, None] = None,
    ):
        if isinstance(date_time, MutableDatetime):
            self._mdt = date_time
        else:
            self._tz = parse_timezone(timezone)
            self._mdt = MutableDatetime(parse_date_time(date_time))

            if self._mdt.tzinfo == None:
                timezoned_str = self._mdt.to_dt().strftime(
                    FormatEnum.FMT_MIL.value
                ) + timezone_to_offset_str(self._tz)
                self._mdt = MutableDatetime(
                    dt.strptime(timezoned_str, FormatEnum.FMT_MIL_TZ.value)
                )

            if timezone != None:
                self._mdt = MutableDatetime(self._mdt.to_dt().astimezone(self._tz))

    def __str__(self) -> str:
        return self._mdt.to_dt().strftime(FormatEnum.FMT_MIL_TZ.value)

    def get(self, part: PartEnum) -> int:
        fmt = PART_FORMAT[part]
        part_str = self._mdt.to_dt().strftime(fmt)
        if part == PartEnum.TZO:
            return offset_str_to_minutes(part_str)
        return int(part_str)

    def clone(self) -> "Diti":
        return Diti(self.__str__())

    def edit(self) -> "DitiEdit":
        return DitiEdit(self._mdt, self._tz)

    def to_dt(self) -> dt:
        return self._mdt.to_dt()


class DitiEdit(Diti):
    __tempdt: dt

    def __init__(
        self,
        date_time: MutableDatetime,
        timezone: str | int | None = None,
    ):
        super().__init__(date_time, timezone)
        self.__tempdt = self._mdt.to_dt()

    def head_of(self, part: PartEnum) -> "DitiEdit":
        diff_calculator = PART_DIFF_CALC[part]
        diff = diff_calculator.diff_to_head(self.__tempdt)
        self.add(PartEnum.MICROSECOND, -diff)
        return self

    def tail_of(self, part: PartEnum) -> "DitiEdit":
        diff_calculator = PART_DIFF_CALC[part]
        diff = diff_calculator.diff_to_tail(self.__tempdt)
        self.add(PartEnum.MICROSECOND, diff)
        return self

    def set(self, part: PartEnum, value: int) -> "DitiEdit":
        current = self.get(part)
        diff = value - current
        self.add(diff, part)
        return self

    def add(self, part: PartEnum, amount: int) -> "DitiEdit":
        self.__tempdt += PART_DELTA[part](amount)
        return self

    def commit(self):
        self._mdt.update(self.__tempdt)

