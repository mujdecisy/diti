from datetime import datetime
from typing import List

import pytz

from diff import PART_DIFF_CALC
from timezones import DitiTimezone
from util import (PART_DELTA, PART_FORMAT, DitiPart, DitiRound,
                  get_daycount_of_month)


class DitiCalcs:
    @staticmethod
    def update(dt: datetime, part: DitiPart, value: int) -> datetime:
        max_val = PART_DIFF_CALC[part].get_max()
        min_val = PART_DIFF_CALC[part].get_min()

        if part == DitiPart.DAYS:
            max_val = get_daycount_of_month(dt.month, dt.year)

        if value > max_val or value < min_val:
            raise ValueError(f"{part.name} must be between {min_val} - {max_val}")
        current = DitiCalcs.get(dt, part)
        diff = value - current
        return DitiCalcs.add(dt, part, diff)

    @staticmethod
    def add(dt: datetime, part: DitiPart, amount: int) -> datetime:
        return dt + PART_DELTA[part](amount)

    @staticmethod
    def head_of(dt: datetime, part: DitiPart) -> datetime:
        diff_calculator = PART_DIFF_CALC[part]
        diff = diff_calculator.diff_to_head(dt)
        return DitiCalcs.add(dt, DitiPart.MICROSECONDS, -diff)

    @staticmethod
    def tail_of(dt: datetime, part: DitiPart) -> datetime:
        diff_calculator = PART_DIFF_CALC[part]
        diff = diff_calculator.diff_to_tail(dt)
        return DitiCalcs.add(dt, DitiPart.MICROSECONDS, diff)

    @staticmethod
    def align_to(
        dt: datetime, part: DitiPart, reference: int, round_mode: DitiRound
    ) -> datetime:
        max_val = PART_DIFF_CALC[part].get_max()
        min_val = PART_DIFF_CALC[part].get_min()
        if reference > max_val or reference < min_val:
            raise ValueError(f"{part.name} must be between {min_val} - {max_val}")

        actual = DitiCalcs.get(dt, part)
        diff = -(actual % reference)
        if round_mode == DitiRound.ROUND_UP:
            diff = reference + diff
        return DitiCalcs.add(dt, part, diff)

    @staticmethod
    def timezone_change(dt: datetime, timezone: DitiTimezone) -> datetime:
        ts = dt.timestamp()
        return dt.fromtimestamp(ts).astimezone(pytz.timezone(timezone.value))

    @staticmethod
    def timezone_update(dt: datetime, timezone: DitiTimezone) -> datetime:
        offset_src = dt.utcoffset()
        if offset_src != None:
            offset_src = offset_src.total_seconds()

        offset_dst = (
            pytz.timezone(timezone.value)
            .utcoffset(datetime.fromtimestamp(dt.timestamp()))
            .total_seconds()
        )

        offset = offset_dst - offset_src

        newdt = DitiCalcs.timezone_change(dt, timezone)
        return DitiCalcs.add(newdt, DitiPart.SECONDS, -offset)

    # --------------------------------------------------------------------------
    @staticmethod
    def get(dt: datetime, part: DitiPart) -> int:
        fmt = PART_FORMAT[part]
        part_str = dt.strftime(fmt)
        return int(part_str)

    @staticmethod
    def diff(from_dt: datetime, to_dt: datetime, part: DitiPart) -> int:
        from_dt_head = DitiCalcs.head_of(from_dt, part)
        to_dt_head = DitiCalcs.head_of(to_dt, part)

        if part == DitiPart.YEARS:
            return DitiCalcs.get(to_dt_head, part) - DitiCalcs.get(from_dt_head, part)
        elif part in [DitiPart.MONTHS, DitiPart.WEEKS]:
            year_diff = DitiCalcs.get(to_dt_head, DitiPart.YEARS) - DitiCalcs.get(
                from_dt_head, DitiPart.YEARS
            )
            return year_diff * (12 if part == DitiPart.MONTHS else 52) - (
                DitiCalcs.get(to_dt_head, part) - DitiCalcs.get(from_dt_head, part)
            )
        else:
            from_ts = from_dt_head.timestamp()
            to_ts = to_dt_head.timestamp()
            seconds_multiplier = (
                PART_DIFF_CALC[part].get_microsecond_multiplier() / 1_000_000
            )
            return (to_ts - from_ts) // seconds_multiplier

    # --------------------------------------------------------------------------
    @staticmethod
    def get_closest_to(
        dt: datetime, dt_list: List[datetime], already_sorted: bool = False
    ) -> [datetime, int]:
        if not already_sorted:
            dt_list = sorted(dt_list)
        pass
