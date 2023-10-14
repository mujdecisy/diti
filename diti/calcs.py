from datetime import datetime, tzinfo
from typing import Union

import pytz

from diti.part_obj import PART
from diti.util import (
    PART_DELTA,
    PART_FORMAT,
    DitiParts,
    DitiRound,
    get_daycount_of_month,
)


class DitiCalcs:
    @staticmethod
    def update(dt: datetime, part: DitiParts, value: int) -> datetime:
        max_val = PART[part].get_max()
        min_val = PART[part].get_min()

        if part == DitiParts.DAYS:
            max_val = get_daycount_of_month(dt.month, dt.year)

        if value > max_val or value < min_val:
            raise ValueError(f"{part.name} must be between {min_val} - {max_val}")
        current = DitiCalcs.get(dt, part)
        diff = value - current
        return DitiCalcs.add(dt, part, diff)

    @staticmethod
    def add(dt: datetime, part: DitiParts, amount: int) -> datetime:
        return dt + PART_DELTA[part](amount)

    @staticmethod
    def head_of(dt: datetime, part: DitiParts) -> datetime:
        diff_calculator = PART[part]
        diff = diff_calculator.diff_to_head(dt)
        return DitiCalcs.add(dt, DitiParts.MICROSECONDS, -diff)

    @staticmethod
    def tail_of(dt: datetime, part: DitiParts) -> datetime:
        diff_calculator = PART[part]
        diff = diff_calculator.diff_to_tail(dt)
        return DitiCalcs.add(dt, DitiParts.MICROSECONDS, diff)

    @staticmethod
    def align_to(
        dt: datetime, part: DitiParts, reference: int, round_mode: DitiRound
    ) -> datetime:
        max_val = PART[part].get_max()
        min_val = PART[part].get_min()
        if reference > max_val or reference < min_val:
            raise ValueError(f"{part.name} must be between {min_val} - {max_val}")

        actual = DitiCalcs.get(dt, part)
        diff = -(actual % reference)
        if round_mode == DitiRound.ROUND_UP:
            diff = reference + diff
        return DitiCalcs.add(dt, part, diff)

    @staticmethod
    def timezone_change(
        dt: datetime, timezone: Union[str, tzinfo]
    ) -> datetime:
        ts = dt.timestamp()
        tz = (
            pytz.timezone(timezone)
            if isinstance(timezone, str)
            else timezone
        )
        return dt.fromtimestamp(ts).astimezone(tz)

    @staticmethod
    def timezone_update(
        dt: datetime, timezone: Union[str, tzinfo]
    ) -> datetime:
        offset_src = dt.utcoffset()
        if offset_src != None:
            offset_src = offset_src.total_seconds()
        else:
            offset_src = 0

        tz = (
            pytz.timezone(timezone)
            if isinstance(timezone, str)
            else timezone
        )

        offset_dst = tz.utcoffset(
            datetime.fromtimestamp(dt.timestamp())
        ).total_seconds()

        offset = offset_dst - offset_src

        newdt = DitiCalcs.timezone_change(dt, timezone)
        return DitiCalcs.add(newdt, DitiParts.SECONDS, -offset)

    # --------------------------------------------------------------------------
    @staticmethod
    def get(dt: datetime, part: DitiParts) -> int:
        fmt = PART_FORMAT[part]
        part_str = dt.strftime(fmt)
        return int(part_str)

    @staticmethod
    def diff(from_dt: datetime, to_dt: datetime, part: DitiParts) -> int:
        from_dt_head = DitiCalcs.head_of(from_dt, part)
        to_dt_head = DitiCalcs.head_of(to_dt, part)

        if part == DitiParts.YEARS:
            return DitiCalcs.get(to_dt_head, part) - DitiCalcs.get(from_dt_head, part)
        elif part in [DitiParts.MONTHS, DitiParts.WEEKS]:
            year_diff = DitiCalcs.get(to_dt_head, DitiParts.YEARS) - DitiCalcs.get(
                from_dt_head, DitiParts.YEARS
            )
            return year_diff * (12 if part == DitiParts.MONTHS else 52) - (
                DitiCalcs.get(to_dt_head, part) - DitiCalcs.get(from_dt_head, part)
            )
        else:
            from_ts = from_dt_head.timestamp()
            to_ts = to_dt_head.timestamp()
            seconds_multiplier = PART[part].get_microsecond_multiplier() / 1_000_000
            return (to_ts - from_ts) // seconds_multiplier
