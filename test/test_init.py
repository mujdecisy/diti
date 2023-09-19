from unittest import TestCase

import pytz

from diti import Diti
from datetime import datetime as dt


class TestInit(TestCase):
    def test__init__when_isostr_year(self):
        o = Diti("2023")
        expected = "2023-01-01T00:00:00.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023+0300")
        expected = "2023-01-01T00:00:00.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_month(self):
        o = Diti("2023-02")
        expected = "2023-02-01T00:00:00.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-0300")
        expected = "2023-02-01T00:00:00.000000-0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_day(self):
        o = Diti("2023-02-03")
        expected = "2023-02-03T00:00:00.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-03+0300")
        expected = "2023-02-03T00:00:00.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_hour(self):
        o = Diti("2023-02-03T04")
        expected = "2023-02-03T04:00:00.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-03T04+0300")
        expected = "2023-02-03T04:00:00.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_min(self):
        o = Diti("2023-02-03T04:05")
        expected = "2023-02-03T04:05:00.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-03T04:05+0300")
        expected = "2023-02-03T04:05:00.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_sec(self):
        o = Diti("2023-02-03T04:05:06")
        expected = "2023-02-03T04:05:06.000000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-03T04:05:06+0300")
        expected = "2023-02-03T04:05:06.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_isostr_mil(self):
        o = Diti("2023-02-03T04:05:06.007000")
        expected = "2023-02-03T04:05:06.007000+0000"
        self.assertEqual(str(o), expected)

        o = Diti("2023-02-03T04:05:06.007000+0300")
        expected = "2023-02-03T04:05:06.007000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_dtobj(self):
        dtobj = dt(year=2023, month=2, day=3, tzinfo=pytz.UTC)
        o = Diti(dtobj)
        expected = "2023-02-03T00:00:00.000000+0000"
        self.assertEqual(str(o), expected)

        dtobj = dtobj.astimezone(pytz.timezone("Europe/Istanbul"))
        o = Diti(dtobj)
        expected = "2023-02-03T03:00:00.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_timestamp(self):
        o = Diti(1694184183)
        expected = "2023-09-08T14:43:03.000000+0000"
        self.assertEqual(str(o), expected)

    def test__init__when_timestamp_with_tz_offset_str(self):
        o = Diti(1694184183, "+0300")
        expected = "2023-09-08T17:43:03.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_timestamp_with_tz_name(self):
        o = Diti(1694184183, "Europe/Istanbul")
        expected = "2023-09-08T17:43:03.000000+0300"
        self.assertEqual(str(o), expected)

    def test__init__when_timestamp_with_tz_offset_min(self):
        o = Diti(1694184183, -180)
        expected = "2023-09-08T11:43:03.000000-0300"
        self.assertEqual(str(o), expected)

    def test__init__when_str_with_tz_offset_min(self):
        o = Diti("2023-01-02T06:04:05.006000+0300", -180)
        expected = "2023-01-02T00:04:05.006000-0300"
        self.assertEqual(str(o), expected)

    def test__init__when_str_wo_tz_and_tz_with_offset_str(self):
        o = Diti("2023-01-02T06:04:05.006000", "+0300")
        expected = "2023-01-02T06:04:05.006000+0300"
        self.assertEqual(str(o), expected)
