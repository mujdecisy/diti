from datetime import datetime as dt
from typing import Dict

from diti.util import DitiParts, get_daycount_of_month

class DitiPart:
    def diff_to_head(self, val: dt) -> int:
        raise NotImplementedError()

    def diff_to_tail(self, val: dt) -> int:
        raise NotImplementedError()

    def get_min(_) -> int:
        raise NotImplementedError()

    def get_max(_) -> int:
        raise NotImplementedError()

    def get_microsecond_multiplier(_) -> int:
        raise NotImplementedError()

    def get_lower_part(_) -> "_DitiPart":
        raise NotImplementedError()

    def capture_part(_, datetime: dt) -> int:
        raise NotImplementedError()

class _DitiPart(DitiPart):
    def diff_to_head(self, val: dt) -> int:
        diff = self.get_lower_part().diff_to_head(val)
        lower = self.get_lower_part()
        addition = lower.capture_part(val) - lower.get_min()
        diff += addition * lower.get_microsecond_multiplier()
        return diff

    def diff_to_tail(self, val: dt) -> int:
        diff = self.get_lower_part().diff_to_tail(val)
        lower = self.get_lower_part()
        addition = lower.get_max() - lower.capture_part(val)
        diff += addition * lower.get_microsecond_multiplier()
        return diff

    def get_min(_) -> int:
        raise NotImplementedError()

    def get_max(_) -> int:
        raise NotImplementedError

    def get_microsecond_multiplier(_) -> int:
        raise NotImplementedError

    def get_lower_part(_) -> "_DitiPart":
        raise NotImplementedError

    def capture_part(_, datetime: dt) -> int:
        raise NotImplementedError()


class _DitiPartNone(_DitiPart):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 0

    def get_lower_part(_) -> _DitiPart:
        return None

    def get_microsecond_multiplier(_) -> int:
        return 0

    def diff_to_head(self, val: dt) -> int:
        return 0

    def diff_to_tail(self, val: dt) -> int:
        return 0

    def capture_part(_, datetime: dt) -> int:
        return 0


class _DitiPartMicrosecond(_DitiPart):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 999999

    def get_lower_part(_) -> _DitiPart:
        return PART_NONE

    def get_microsecond_multiplier(_) -> int:
        return 1

    def capture_part(_, datetime: dt) -> int:
        return datetime.microsecond


class _DitiPartSecond(_DitiPart):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 59

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.MICROSECONDS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000

    def capture_part(_, datetime: dt) -> int:
        return datetime.second


class _DitiPartMinute(_DitiPart):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 59

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.SECONDS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60

    def capture_part(_, datetime: dt) -> int:
        return datetime.minute


class _DitiPartHour(_DitiPart):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 23

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.MINUTES]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60 * 60

    def capture_part(_, datetime: dt) -> int:
        return datetime.hour


class _DitiPartDay(_DitiPart):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 31

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.HOURS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60 * 60 * 24

    def capture_part(_, datetime: dt) -> int:
        return datetime.day


class _DitiPartWeek(_DitiPart):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 52

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.DAYS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60 * 60 * 24 * 7

    def capture_part(_, datetime: dt) -> int:
        return datetime.day

    def diff_to_head(self, val: dt) -> int:
        lower = self.get_lower_part()
        diff = lower.diff_to_head(val)
        additional = val.weekday() * lower.get_microsecond_multiplier()
        diff += additional
        return diff

    def diff_to_tail(self, val: dt) -> int:
        lower = self.get_lower_part()
        diff = lower.diff_to_tail(val)
        additional = (6 - val.weekday()) * lower.get_microsecond_multiplier()
        diff += additional
        return diff


class _DitiPartMonth(_DitiPart):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 12

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.DAYS]

    def capture_part(_, datetime: dt) -> int:
        return datetime.month

    def diff_to_tail(self, val: dt) -> int:
        lower = self.get_lower_part()
        diff = lower.diff_to_tail(val)
        day_count = get_daycount_of_month(val.month, val.year)
        additional = (day_count - val.day) * lower.get_microsecond_multiplier()
        diff += additional
        return diff


class _DitiPartYear(_DitiPart):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 9999

    def get_lower_part(_) -> _DitiPart:
        return PART[DitiParts.MONTHS]

    def capture_part(_, datetime: dt) -> int:
        return datetime.year

    def diff_to_head(self, val: dt) -> int:
        lower = self.get_lower_part()
        month_val = lower.capture_part(val)
        day_count = 0
        for i in range(1, month_val):
            day_count += get_daycount_of_month(i, val.year)
        diff = lower.diff_to_head(val)
        additional = day_count * lower.get_lower_part().get_microsecond_multiplier()
        diff += additional
        return diff

    def diff_to_tail(self, val: dt) -> int:
        lower = self.get_lower_part()
        month_val = lower.capture_part(val)
        day_count = 0
        for i in range(month_val + 1, 13):
            day_count += get_daycount_of_month(i, val.year)
        diff = lower.diff_to_tail(val)
        additional = day_count * lower.get_lower_part().get_microsecond_multiplier()
        diff += additional
        return diff

PART_NONE: DitiPart = _DitiPartNone()

PART: Dict[DitiParts, DitiPart] = {
    DitiParts.MICROSECONDS: _DitiPartMicrosecond(),
    DitiParts.SECONDS: _DitiPartSecond(),
    DitiParts.MINUTES: _DitiPartMinute(),
    DitiParts.HOURS: _DitiPartHour(),
    DitiParts.DAYS: _DitiPartDay(),
    DitiParts.WEEKS: _DitiPartWeek(),
    DitiParts.MONTHS: _DitiPartMonth(),
    DitiParts.YEARS: _DitiPartYear(),
}
