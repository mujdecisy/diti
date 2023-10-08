from datetime import datetime as dt
from typing import Dict

from util import DitiPart, get_daycount_of_month

class DitiDiff:
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

    def get_lower_part(_) -> "_DiffCalc":
        raise NotImplementedError()

    def capture_part(_, datetime: dt) -> int:
        raise NotImplementedError()

class _DiffCalc(DitiDiff):
    def diff_to_head(self, val: dt) -> int:
        diff = self.get_lower_part().diff_to_head(val)
        lower = self.get_lower_part()
        addition = lower.capture_part(val) - lower.get_min()
        print(
            self.__class__.__name__, diff, addition, lower.get_microsecond_multiplier()
        )
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

    def get_lower_part(_) -> "_DiffCalc":
        raise NotImplementedError

    def capture_part(_, datetime: dt) -> int:
        raise NotImplementedError()


class _DiffCalcNone(_DiffCalc):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 0

    def get_lower_part(_) -> _DiffCalc:
        return None

    def get_microsecond_multiplier(_) -> int:
        return 0

    def diff_to_head(self, val: dt) -> int:
        return 0

    def diff_to_tail(self, val: dt) -> int:
        return 0

    def capture_part(_, datetime: dt) -> int:
        return 0


class _DiffCalcMicrosecond(_DiffCalc):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 999999

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC_NONE

    def get_microsecond_multiplier(_) -> int:
        return 1

    def capture_part(_, datetime: dt) -> int:
        return datetime.microsecond


class _DiffCalcSecond(_DiffCalc):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 59

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.MICROSECONDS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000

    def capture_part(_, datetime: dt) -> int:
        return datetime.second


class _DiffCalcMinute(_DiffCalc):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 59

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.SECONDS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60

    def capture_part(_, datetime: dt) -> int:
        return datetime.minute


class _DiffCalcHour(_DiffCalc):
    def get_min(_) -> int:
        return 0

    def get_max(_) -> int:
        return 23

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.MINUTES]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60 * 60

    def capture_part(_, datetime: dt) -> int:
        return datetime.hour


class _DiffCalcDay(_DiffCalc):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 31

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.HOURS]

    def get_microsecond_multiplier(_) -> int:
        return 1_000_000 * 60 * 60 * 24

    def capture_part(_, datetime: dt) -> int:
        return datetime.day


class _DiffCalcWeek(_DiffCalc):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 52

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.DAYS]

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


class _DiffCalcMonth(_DiffCalc):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 12

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.DAYS]

    def capture_part(_, datetime: dt) -> int:
        return datetime.month

    def diff_to_tail(self, val: dt) -> int:
        lower = self.get_lower_part()
        diff = lower.diff_to_tail(val)
        day_count = get_daycount_of_month(val.month, val.year)
        additional = (day_count - val.day) * lower.get_microsecond_multiplier()
        diff += additional
        return diff


class _DiffCalcYear(_DiffCalc):
    def get_min(_) -> int:
        return 1

    def get_max(_) -> int:
        return 9999

    def get_lower_part(_) -> _DiffCalc:
        return PART_DIFF_CALC[DitiPart.MONTHS]

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

PART_DIFF_CALC_NONE: DitiDiff = _DiffCalcNone()

PART_DIFF_CALC: Dict[DitiPart, DitiDiff] = {
    DitiPart.MICROSECONDS: _DiffCalcMicrosecond(),
    DitiPart.SECONDS: _DiffCalcSecond(),
    DitiPart.MINUTES: _DiffCalcMinute(),
    DitiPart.HOURS: _DiffCalcHour(),
    DitiPart.DAYS: _DiffCalcDay(),
    DitiPart.WEEKS: _DiffCalcWeek(),
    DitiPart.MONTHS: _DiffCalcMonth(),
    DitiPart.YEARS: _DiffCalcYear(),
}
