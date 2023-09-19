from unittest import TestCase

from diti import Diti
from util import PartEnum


class TestEdit(TestCase):
    def test__edit__not_committed(self):
        o = Diti("2023")
        o.edit().add(PartEnum.DAY, 1)
        self.assertTrue(o.__str__().startswith("2023-01-01"))

    def test__edit__add_year(self):
        o = Diti("2023")
        o.edit().add(PartEnum.YEAR, 1).commit()
        self.assertTrue(o.__str__().startswith("2024-01-01"))

    def test__edit__subtract_year(self):
        o = Diti("2023")
        o.edit().add(PartEnum.YEAR, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-01-01"))

    def test__edit__add_month(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MONTH, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-02-01"))

    def test__edit__subtract_month(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MONTH, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-01"))

    def test__edit__add_day(self):
        o = Diti("2023")
        o.edit().add(PartEnum.DAY, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-02"))

    def test__edit__subtract_day(self):
        o = Diti("2023")
        o.edit().add(PartEnum.DAY, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31"))

    def test__edit__add_hour(self):
        o = Diti("2023")
        o.edit().add(PartEnum.HOUR, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T01"))

    def test__edit__subtract_hour(self):
        o = Diti("2023")
        o.edit().add(PartEnum.HOUR, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23"))

    def test__edit__add_minute(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MINUTE, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:01"))

    def test__edit__subtract_minute(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MINUTE, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59"))

    def test__edit__add_second(self):
        o = Diti("2023")
        o.edit().add(PartEnum.SECOND, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:00:01"))

    def test__edit__subtract_second(self):
        o = Diti("2023")
        o.edit().add(PartEnum.SECOND, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59:59"))

    def test__edit__add_microsecond(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MICROSECOND, 1).commit()
        self.assertTrue(o.__str__().startswith("2023-01-01T00:00:00.000001"))

    def test__edit__subtract_microsecond(self):
        o = Diti("2023")
        o.edit().add(PartEnum.MICROSECOND, -1).commit()
        self.assertTrue(o.__str__().startswith("2022-12-31T23:59:59.999999"))

    def test__edit__multiple_steps(self):
        o = Diti("2023")
        o.edit()\
            .add(PartEnum.MONTH, 1)\
            .add(PartEnum.DAY, -1)\
            .add(PartEnum.HOUR, 1)\
            .add(PartEnum.MINUTE, -1)\
            .add(PartEnum.SECOND, 1)\
            .commit()
        self.assertTrue(o.__str__().startswith("2023-01-31T00:59:01"))

    def test__edit__headof_year(self):
        o = Diti("2023-07")
        o.edit().head_of(PartEnum.YEAR).commit()
        self.assertEquals( o.__str__(), '2023-01-01T00:00:00.000000+0000' )

    def test__edit__tailof_year(self):
        o = Diti("2023-07")
        o.edit().tail_of(PartEnum.YEAR).commit()
        self.assertEquals( o.__str__(), '2023-12-31T23:59:59.999999+0000' )

    def test__edit__headof_month(self):
        o = Diti("2023-07-15")
        o.edit().head_of(PartEnum.MONTH).commit()
        self.assertEquals( o.__str__(), '2023-07-01T00:00:00.000000+0000' )

    def test__edit__tailof_month(self):
        o = Diti("2023-07-15")
        o.edit().tail_of(PartEnum.MONTH).commit()
        self.assertEquals( o.__str__(), '2023-07-31T23:59:59.999999+0000' )

    def test__edit__headof_week(self):
        o = Diti("2023-07-15")
        o.edit().head_of(PartEnum.WEEK).commit()
        self.assertEquals( o.__str__(), '2023-07-10T00:00:00.000000+0000' )

    def test__edit__tailof_week(self):
        o = Diti("2023-07-15")
        o.edit().tail_of(PartEnum.WEEK).commit()
        self.assertEquals( o.__str__(), '2023-07-16T23:59:59.999999+0000' )

    def test__edit__headof_day(self):
        o = Diti("2023-07-15T10")
        o.edit().head_of(PartEnum.DAY).commit()
        self.assertEquals( o.__str__(), '2023-07-15T00:00:00.000000+0000' )

    def test__edit__tailof_day(self):
        o = Diti("2023-07-15T10")
        o.edit().tail_of(PartEnum.DAY).commit()
        self.assertEquals( o.__str__(), '2023-07-15T23:59:59.999999+0000' )

    def test__edit__headof_hour(self):
        o = Diti("2023-07-15T10:25")
        o.edit().head_of(PartEnum.HOUR).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:00:00.000000+0000' )

    def test__edit__tailof_hour(self):
        o = Diti("2023-07-15T10:25")
        o.edit().tail_of(PartEnum.HOUR).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:59:59.999999+0000' )

    def test__edit__headof_minute(self):
        o = Diti("2023-07-15T10:25:35")
        o.edit().head_of(PartEnum.MINUTE).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:00.000000+0000' )

    def test__edit__tailof_minute(self):
        o = Diti("2023-07-15T10:25:35")
        o.edit().tail_of(PartEnum.MINUTE).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:59.999999+0000' )

    def test__edit__headof_second(self):
        o = Diti("2023-07-15T10:25:35.501501")
        o.edit().head_of(PartEnum.SECOND).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.000000+0000' )

    def test__edit__tailof_second(self):
        o = Diti("2023-07-15T10:25:35.501501")
        o.edit().tail_of(PartEnum.SECOND).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.999999+0000' )

    def test__edit__headof_microsecond(self):
        o = Diti("2023-07-15T10:25:35.500500")
        o.edit().head_of(PartEnum.MICROSECOND).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.500500+0000' )

    def test__edit__tailof_microsecond(self):
        o = Diti("2023-07-15T10:25:35.500500")
        o.edit().tail_of(PartEnum.MICROSECOND).commit()
        self.assertEquals( o.__str__(), '2023-07-15T10:25:35.500500+0000' )

