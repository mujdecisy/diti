from datetime import datetime
from typing import List

from diti.calcs import DitiCalcs
from diti.timezones import DitiTimezone
from diti.util import DitiParts, DitiRound, parse_date_time


class DitiOp:
    def _exec(self, dt: datetime) -> datetime:
        raise NotImplementedError()


class DitiOpUpdate(DitiOp):
    def __init__(self, part: DitiParts, value: int) -> None:
        self.__part = part
        self.__value = value

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.update(dt, self.__part, self.__value)


class DitiOpAdd(DitiOp):
    def __init__(self, part: DitiParts, amount: int) -> None:
        self.__part = part
        self.__amount = amount

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.add(dt, self.__part, self.__amount)


class DitiOpHeadOf(DitiOp):
    def __init__(self, part: DitiParts) -> None:
        self.__part = part

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.head_of(dt, self.__part)


class DitiOpTailOf(DitiOp):
    def __init__(self, part: DitiParts) -> None:
        self.__part = part

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.tail_of(dt, self.__part)


class DitiOpAlignTo(DitiOp):
    def __init__(
        self,
        part: DitiParts,
        reference: int,
        round_mode: DitiRound = DitiRound.ROUND_DOWN,
    ) -> None:
        self.__part = part
        self.__reference = reference
        self.__round_mode = round_mode

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.align_to(dt, self.__part, self.__reference, self.__round_mode)

class DitiOpTimezoneChange(DitiOp):
    def __init__(self, timezone: DitiTimezone) -> None:
        self.__timeozone = timezone

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.timezone_change(dt, self.__timeozone)


class DitiOpTimezoneUpdate(DitiOp):
    def __init__(self, timezone: DitiTimezone) -> None:
        self.__timeozone = timezone

    def _exec(self, dt: datetime) -> datetime:
        return DitiCalcs.timezone_update(dt, self.__timeozone)

class DitiOps:
    UPDATE = DitiOpUpdate
    ADD = DitiOpAdd
    HEAD_OF = DitiOpHeadOf
    TAIL_OF = DitiOpTailOf
    ALIGN_TO = DitiOpAlignTo
    TZ_CHANGE = DitiOpTimezoneChange
    TZ_UPDATE = DitiOpTimezoneUpdate

def diti_op(dt: None | datetime | str | int | float, ops: List[DitiOp]) -> datetime:
    dt = parse_date_time(dt)
    for op in ops:
        dt = op._exec(dt)
    return dt
