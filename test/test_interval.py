from datetime import datetime, timezone as dt_tz
from unittest import TestCase
from bson import utc

from diti.diti_interval import DitiInterval
from diti.diti_obj import Diti
from diti.util import DitiParts


class TestInterval(TestCase):
    def test__overlapped__with_overlapped_timeslots(self):
        from_pivot = datetime.fromtimestamp(5)
        to_pivot = datetime.fromtimestamp(10)
        other_timeslots = [
            [datetime.fromtimestamp(1), datetime.fromtimestamp(3)],
            [datetime.fromtimestamp(2), datetime.fromtimestamp(6)],
            [datetime.fromtimestamp(4), datetime.fromtimestamp(12)],
            [datetime.fromtimestamp(7), datetime.fromtimestamp(9)],
            [datetime.fromtimestamp(8), datetime.fromtimestamp(14)],
            [datetime.fromtimestamp(11), datetime.fromtimestamp(17)],
        ]

        indexes = DitiInterval.overlapped_timeslots(
            from_pivot, to_pivot, other_timeslots
        )
        expected = [1, 2, 3, 4]
        self.assertEqual(indexes, expected)

    def test__overlapped__with_infinite_timeslots(self):
        from_pivot = datetime.fromtimestamp(5)
        to_pivot = datetime.fromtimestamp(10)
        other_timeslots = [
            [None, None],
            [datetime.fromtimestamp(6), None],
            [None, datetime.fromtimestamp(6)],
            [None, datetime.fromtimestamp(3)],
            [datetime.fromtimestamp(11), None],
        ]

        indexes = DitiInterval.overlapped_timeslots(
            from_pivot, to_pivot, other_timeslots
        )
        expected = [
            0,
            1,
            2,
        ]
        self.assertEqual(indexes, expected)

    def test__divide_into_timeslots__microseconds(self):
        from_pivot = Diti("2023-07-15T12:30:15.500")
        to_pivot = Diti("2023-07-15T12:30:15.600")

        actual = DitiInterval.divide_into_timeslots(
            from_pivot.to_dt(), to_pivot.to_dt(), DitiParts.MICROSECONDS, 25_000, dt_tz.utc
        )

        expected = [
            Diti("2023-07-15T12:30:15.500").to_dt(),
            Diti("2023-07-15T12:30:15.525").to_dt(),
            Diti("2023-07-15T12:30:15.550").to_dt(),
            Diti("2023-07-15T12:30:15.575").to_dt(),
            Diti("2023-07-15T12:30:15.600").to_dt(),
        ]

        self.assertEqual(actual, expected)


    def test__divide_into_timeslots__minutes(self):
        from_pivot = Diti("2023-07-15T12:30:15")
        to_pivot = Diti("2023-07-15T18:00:15")

        actual = DitiInterval.divide_into_timeslots(
            from_pivot.to_dt(), to_pivot.to_dt(), DitiParts.MINUTES, 90, dt_tz.utc
        )

        expected = [
            Diti("2023-07-15T12:30:15").to_dt(),
            Diti("2023-07-15T14:00:15").to_dt(),
            Diti("2023-07-15T15:30:15").to_dt(),
            Diti("2023-07-15T17:00:15").to_dt(),
        ]

        self.assertEqual(actual, expected)

    def test__divide_into_timeslots__weeks(self):
        from_pivot = Diti("2023-07-15T12:30:15")
        to_pivot = Diti("2023-08-15T12:30:15")

        actual = DitiInterval.divide_into_timeslots(
            from_pivot.to_dt(), to_pivot.to_dt(), DitiParts.WEEKS, 1, dt_tz.utc
        )

        expected = [
            Diti("2023-07-15T12:30:15").to_dt(),
            Diti("2023-07-22T12:30:15").to_dt(),
            Diti("2023-07-29T12:30:15").to_dt(),
            Diti("2023-08-05T12:30:15").to_dt(),
            Diti("2023-08-12T12:30:15").to_dt(),
        ]

        self.assertEqual(actual, expected)


    def test__divide_into_timeslots__months(self):
        from_pivot = Diti("2023-07-15T12:30:15")
        to_pivot = Diti("2023-12-15T12:30:15")

        actual = DitiInterval.divide_into_timeslots(
            from_pivot.to_dt(), to_pivot.to_dt(), DitiParts.MONTHS, 1, dt_tz.utc
        )

        expected = [
            Diti("2023-07-15T12:30:15").to_dt(),
            Diti("2023-08-15T12:30:15").to_dt(),
            Diti("2023-09-15T12:30:15").to_dt(),
            Diti("2023-10-15T12:30:15").to_dt(),
            Diti("2023-11-15T12:30:15").to_dt(),
            Diti("2023-12-15T12:30:15").to_dt(),
        ]

        self.assertEqual(actual, expected)


    def test__closest_time(self):
        pivot = datetime.fromtimestamp(5)
        dt_list = [
            datetime.fromtimestamp(1),
            datetime.fromtimestamp(3),
            datetime.fromtimestamp(6),
            datetime.fromtimestamp(7),
        ]
        actual = DitiInterval.closest_time(pivot, dt_list)
        self.assertEqual(actual, 2)