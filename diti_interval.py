from datetime import datetime, tzinfo
from typing import List, Tuple
from calcs import DitiCalcs

from util import DitiParts

MAX_TIMESTAMP = 99999999999.999999


class DitiInterval:
    @staticmethod
    def overlapped_timeslots(
        from_pivot_dt: datetime,
        to_pivot_dt: datetime,
        other_timeslots: List[Tuple[datetime, datetime]]
    ) -> List[int]:
        ts_from = from_pivot_dt.timestamp()
        ts_to = (
            to_pivot_dt.timestamp()
            if isinstance(to_pivot_dt, datetime)
            else MAX_TIMESTAMP
        )
        overlapped = []
        for ix, e in enumerate(other_timeslots):
            ts_from_timeslot = e[0].timestamp() if isinstance(e[0], datetime) else 0
            ts_to_timeslot = (
                e[1].timestamp() if isinstance(e[1], datetime) else MAX_TIMESTAMP
            )
            if ts_from <= ts_to_timeslot and ts_to >= ts_from_timeslot:
                overlapped.append(ix)

        return overlapped

    @staticmethod
    def divide_into_timeslots(
        from_pivot_dt: datetime,
        to_pivot_dt: datetime,
        interval: DitiParts,
        amount: int,
        tz: tzinfo = None,
    ) -> List[datetime]:
        from_dt = DitiCalcs.timezone_update(from_pivot_dt, tz)
        to_dt = DitiCalcs.timezone_update(to_pivot_dt, tz)

        steps = []
        while from_dt <= to_dt:
            steps.append(from_dt)
            from_dt = DitiCalcs.add(steps[-1], interval, amount)
            if tz != None:
                from_dt = DitiCalcs.timezone_update(from_dt, tz)

        return steps

    @staticmethod
    def closest_time(
        pivot_dt: datetime,
        dt_list: List[datetime]
    ) -> int:
        # todo(mujdecisy) : add tree search logic if dt_list is sorted
        ix = -1
        min_distance = float("inf")
        pivot_ts = pivot_dt.timestamp()
        for i in range(len(dt_list)):
            distance = abs(pivot_ts - dt_list[i].timestamp())
            if min_distance > distance:
                ix = i
                min_distance = distance
        return ix