from unittest import TestCase

from diti.diti_obj import Diti
from diti.util import DitiParts


class TestEdit(TestCase):
    def test__edit__not_committed(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.DAYS, 1)
        self.assertTrue(o.__str__().startswith("2023-01-01"))

    def test__edit__add_year(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.YEARS, 1).commit()
        self.assertTrue(o.__str__().startswith("2024-01-01"))

    def test__edit__subtract_year(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.YEARS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-01-01"))

    def test__edit__add_month(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MONTHS, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-02-01"))

    def test__edit__subtract_month(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MONTHS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-01"))

    def test__edit__add_day(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.DAYS, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-02"))

    def test__edit__subtract_day(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.DAYS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31"))

    def test__edit__add_hour(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.HOURS, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T01"))

    def test__edit__subtract_hour(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.HOURS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23"))

    def test__edit__add_minute(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MINUTES, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:01"))

    def test__edit__subtract_minute(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MINUTES, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59"))

    def test__edit__add_second(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.SECONDS, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:00:01"))

    def test__edit__subtract_second(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.SECONDS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59:59"))

    def test__edit__add_microsecond(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MICROSECONDS, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:00:00.000001"))

    def test__edit__subtract_microsecond(self):
        o = Diti("2023-01-01")
        o.edit().add(DitiParts.MICROSECONDS, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59:59.999999"))

    def test__edit__multiple_steps(self):
        o = Diti("2023-01-01")
        o.edit()\
            .add(DitiParts.MONTHS, 1)\
            .add(DitiParts.DAYS, -1)\
            .add(DitiParts.HOURS, 1)\
            .add(DitiParts.MINUTES, -1)\
            .add(DitiParts.SECONDS, 1)\
            .commit()
        self.assertTrue(o.__str__().startswith("2023-01-31T00:59:01"))

    def test__edit__headof_year(self):
        o = Diti("2023-07-01")
        o.edit().head_of(DitiParts.YEARS).commit()
        self.assertEquals( o.__str__(), '2023-01-01T00:00:00+00:00' )

    def test__edit__tailof_year(self):
        o = Diti("2023-07-01")
        o.edit().tail_of(DitiParts.YEARS).commit()
        self.assertEquals( o.__str__(), '2023-12-31T23:59:59.999999+00:00' )

    def test__edit__headof_month(self):
        o = Diti("2023-07-15")
        o.edit().head_of(DitiParts.MONTHS).commit()
        self.assertEquals( o.__str__(), '2023-07-01T00:00:00+00:00' )

    def test__edit__tailof_month(self):
        o = Diti("2023-07-15")
        o.edit().tail_of(DitiParts.MONTHS).commit()
        self.assertEquals( o.__str__(), '2023-07-31T23:59:59.999999+00:00' )

    def test__edit__headof_week(self):
        o = Diti("2023-07-15")
        o.edit().head_of(DitiParts.WEEKS).commit()
        self.assertEquals( o.__str__(), '2023-07-10T00:00:00+00:00' )

    def test__edit__tailof_week(self):
        o = Diti("2023-07-15")
        o.edit().tail_of(DitiParts.WEEKS).commit()
        self.assertEquals( o.__str__(), '2023-07-16T23:59:59.999999+00:00' )

    def test__edit__headof_day(self):
        o = Diti("2023-07-15T10")
        o.edit().head_of(DitiParts.DAYS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T00:00:00+00:00' )

    def test__edit__tailof_day(self):
        o = Diti("2023-07-15T10")
        o.edit().tail_of(DitiParts.DAYS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T23:59:59.999999+00:00' )

    def test__edit__headof_hour(self):
        o = Diti("2023-07-15T10:25")
        o.edit().head_of(DitiParts.HOURS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:00:00+00:00' )

    def test__edit__tailof_hour(self):
        o = Diti("2023-07-15T10:25")
        o.edit().tail_of(DitiParts.HOURS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:59:59.999999+00:00' )

    def test__edit__headof_minute(self):
        o = Diti("2023-07-15T10:25:35")
        o.edit().head_of(DitiParts.MINUTES).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:00+00:00' )

    def test__edit__tailof_minute(self):
        o = Diti("2023-07-15T10:25:35")
        o.edit().tail_of(DitiParts.MINUTES).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:59.999999+00:00' )

    def test__edit__headof_second(self):
        o = Diti("2023-07-15T10:25:35.501501")
        o.edit().head_of(DitiParts.SECONDS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35+00:00' )

    def test__edit__tailof_second(self):
        o = Diti("2023-07-15T10:25:35.501501")
        o.edit().tail_of(DitiParts.SECONDS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.999999+00:00' )

    def test__edit__headof_microsecond(self):
        o = Diti("2023-07-15T10:25:35.500500")
        o.edit().head_of(DitiParts.MICROSECONDS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.500500+00:00' )

    def test__edit__tailof_microsecond(self):
        o = Diti("2023-07-15T10:25:35.500500")
        o.edit().tail_of(DitiParts.MICROSECONDS).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.500500+00:00' )

