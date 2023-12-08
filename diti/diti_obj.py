from datetime import datetime as dt
from typing import List, Union

import pytz

from diti.calcs import DitiCalcs
from diti.constants import DitiParts, DitiRound
from diti.diti_ops import DitiOp, diti_op
from diti.util import (
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
            self._mdt = MutableDatetime(parse_date_time(date_time))
            self._tz = parse_timezone(timezone)

            if self._mdt.tzinfo == None:
                timezoned_str = self._mdt.to_dt().isoformat() + timezone_to_offset_str(
                    self._tz, self._mdt.to_dt()
                )
                self._mdt = MutableDatetime(dt.fromisoformat(timezoned_str))

            if timezone != None:
                self._mdt = MutableDatetime(self._mdt.to_dt().astimezone(self._tz))

    def __str__(self) -> str:
        return self._mdt.to_dt().isoformat()

    def get(self, part: DitiParts) -> int:
        return DitiCalcs.get(self._mdt.to_dt(), part)

    def clone(self) -> "Diti":
        return Diti(self.__str__())

    def edit(self) -> "DitiEdit":
        return DitiEdit(self._mdt, self._tz)

    def edit_ops(self, ops: List[DitiOp]) -> None:
        new_dt = diti_op(self._mdt.to_dt(), ops)
        self._mdt.update(new_dt)

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

    def head_of(self, part: DitiParts) -> "DitiEdit":
        self.__tempdt = DitiCalcs.head_of(self.__tempdt, part)
        return self

    def tail_of(self, part: DitiParts) -> "DitiEdit":
        self.__tempdt = DitiCalcs.tail_of(self.__tempdt, part)
        return self

    def update(self, part: DitiParts, value: int) -> "DitiEdit":
        self.__tempdt = DitiCalcs.update(self.__tempdt, part, value)
        return self

    def add(self, part: DitiParts, amount: int) -> "DitiEdit":
        self.__tempdt = DitiCalcs.add(self.__tempdt, part, amount)
        return self

    def align_to(self, part: DitiParts, reference: int, rounding_mode: DitiRound):
        self.__tempdt = DitiCalcs.align_to(
            self.__tempdt, part, reference, rounding_mode
        )
        return self

    def timezone_change(self, timezone: str):
        self.__tempdt = DitiCalcs.timezone_change(self.__tempdt, timezone)
        return self

    def timezone_update(self, timezone: str):
        self.__tempdt = DitiCalcs.timezone_update(self.__tempdt, timezone)
        return self

    def commit(self):
        self._mdt.update(self.__tempdt)
