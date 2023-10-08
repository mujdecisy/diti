from datetime import datetime
from unittest import TestCase

import pytz

from calcs import DitiCalcs
from timezones import DitiTimezone
from util import DitiPart, DitiRound


class TestCalcs(TestCase):
    def test__update__when_val_higher_than_max(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.YEARS, 1_000_000)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MONTHS, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.WEEKS, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.DAYS, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.HOURS, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MINUTES, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.SECONDS, 100)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MICROSECONDS, 10_000_000)

    def test__update__when_val_lower_than_min(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.YEARS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MONTHS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.WEEKS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.DAYS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.HOURS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MINUTES, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.SECONDS, -1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.MICROSECONDS, -1)

    def test__update(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        dt = DitiCalcs.update(dt, DitiPart.YEARS, 2024)
        dt = DitiCalcs.update(dt, DitiPart.MONTHS, 2)
        dt = DitiCalcs.update(dt, DitiPart.DAYS, 2)
        dt = DitiCalcs.update(dt, DitiPart.HOURS, 2)
        dt = DitiCalcs.update(dt, DitiPart.MINUTES, 2)
        dt = DitiCalcs.update(dt, DitiPart.SECONDS, 2)
        dt = DitiCalcs.update(dt, DitiPart.MICROSECONDS, 2)
        expected = datetime(2024, 2, 2, 2, 2, 2, 2)
        self.assertEqual(expected, dt)

    def test__update_week(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        dt = DitiCalcs.update(dt, DitiPart.WEEKS, 1)
        expected = datetime(2023, 1, 8, 1, 1, 1, 1)
        self.assertEqual(expected, dt)

    def test__update__when_leap_year(self):
        dt = datetime(2020, 2, 1, 1, 1, 1, 1)
        dt = DitiCalcs.update(dt, DitiPart.DAYS, 29)
        expected = datetime(2020, 2, 29, 1, 1, 1, 1)
        self.assertEqual(expected, dt)

    def test__update__when_not_leap_year(self):
        dt = datetime(2021, 2, 1, 1, 1, 1, 1)
        with self.assertRaises(ValueError):
            dt = DitiCalcs.update(dt, DitiPart.DAYS, 29)

    def test__add(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        dt = DitiCalcs.add(dt, DitiPart.YEARS, 2)
        dt = DitiCalcs.add(dt, DitiPart.MONTHS, 2)
        dt = DitiCalcs.add(dt, DitiPart.DAYS, 2)
        dt = DitiCalcs.add(dt, DitiPart.HOURS, 2)
        dt = DitiCalcs.add(dt, DitiPart.MINUTES, 2)
        dt = DitiCalcs.add(dt, DitiPart.SECONDS, 2)
        dt = DitiCalcs.add(dt, DitiPart.MICROSECONDS, 2)
        expected = datetime(2025, 3, 3, 3, 3, 3, 3)
        self.assertEqual(dt, expected)

    def test__week(self):
        dt = datetime(2023, 1, 1, 1, 1, 1, 1)
        dt = DitiCalcs.add(dt, DitiPart.WEEKS, 2)
        expected = datetime(2023, 1, 15, 1, 1, 1, 1)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__year(self):
        part = DitiPart.YEARS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 1, 1, 0, 0, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__month(self):
        part = DitiPart.MONTHS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 1, 0, 0, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 31, 23, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__leap_year(self):
        part = DitiPart.MONTHS
        dt = datetime(2020, 2, 3, 3, 3, 3, 3)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2020, 2, 29, 23, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__week(self):
        part = DitiPart.WEEKS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 2, 27, 0, 0, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 5, 23, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__day(self):
        part = DitiPart.DAYS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 3, 0, 0, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 3, 23, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__hour(self):
        part = DitiPart.HOURS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 0, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 59, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__minute(self):
        part = DitiPart.MINUTES
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 0, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 59, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__second(self):
        part = DitiPart.SECONDS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 3, 0)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 3, 999999)
        self.assertEqual(dt, expected)

    def test__head_of__tail_of__microsecond(self):
        part = DitiPart.MICROSECONDS
        dt = datetime(2023, 3, 3, 3, 3, 3, 3)
        dt = DitiCalcs.head_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 3, 3)
        self.assertEqual(dt, expected)
        dt = DitiCalcs.tail_of(dt, part)
        expected = datetime(2023, 3, 3, 3, 3, 3, 3)
        self.assertEqual(dt, expected)

    def test__timezone_change__negative_to_positive(self):
        dt = datetime.fromisoformat("2023-03-03T03:00:00-08:00")
        dt = DitiCalcs.timezone_change(dt, DitiTimezone.Europe__Istanbul)
        expected = "2023-03-03T14:00:00+03:00"
        self.assertEqual(dt.isoformat(), expected)

    def test__timezone_change__postitive_to_negative(self):
        dt = datetime.fromisoformat("2023-03-03T14:00:00+03:00")
        dt = DitiCalcs.timezone_change(dt, DitiTimezone.America__Los_Angeles)
        expected = "2023-03-03T03:00:00-08:00"
        self.assertEqual(dt.isoformat(), expected)

    def test__timezone_update(self):
        dt = datetime.fromisoformat("2023-03-03T03:00:00-08:00")
        dt = DitiCalcs.timezone_update(dt, DitiTimezone.UTC)
        expected = "2023-03-03T03:00:00+00:00"
        self.assertEqual(dt.isoformat(), expected)

    def test__align_to__when_reference_in_scope(self):
        dt = datetime.fromisoformat("2023-03-03T03:03:03+0000")

        actual = DitiCalcs.align_to(dt, DitiPart.SECONDS, 15, DitiRound.ROUND_DOWN)
        expected = datetime.fromisoformat("2023-03-03T03:03:00+0000")
        self.assertEqual(actual, expected)

        actual = DitiCalcs.align_to(dt, DitiPart.SECONDS, 15, DitiRound.ROUND_UP)
        expected = datetime.fromisoformat("2023-03-03T03:03:15+0000")
        self.assertEqual(actual, expected)

    def test__align_to__when_reference_out_of_scope(self):
        dt = datetime.fromisoformat("2023-03-03T03:03:03+0000")

        with self.assertRaises(ValueError):
            DitiCalcs.align_to(dt, DitiPart.HOURS, 36, DitiRound.ROUND_DOWN)

        with self.assertRaises(ValueError):
            DitiCalcs.align_to(dt, DitiPart.MINUTES, 60, DitiRound.ROUND_UP)
