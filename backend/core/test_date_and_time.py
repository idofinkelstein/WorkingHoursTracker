from unittest import TestCase
from datetime import datetime, time, timedelta
from date_and_time import DateHandler
from date_validator import Validator


class Test(TestCase):

    def test_subtract_of_1_day_and_above(self):
        start_date = datetime(2016, 1, 1)
        end_date = datetime(2016, 1, 2, 17, 40, 0)
        delta = timedelta(days=1, hours=17, minutes=40)
        actual = DateHandler.subtract_time(start_date, end_date)
        self.assertEqual(actual, delta)

    def test_subtract_of_less_than_one_day(self):
        start_date = datetime(2019, 1, 1, 9, 22, 0)
        end_date = datetime(2019, 1, 1, 17, 40, 0)
        delta = timedelta(days=0, hours=8, minutes=18)
        actual = DateHandler.subtract_time(start_date, end_date)
        self.assertEqual(actual, delta)

    def test_create_valid_date(self):
        date_str = "20/01/2023 10:30"
        expected = datetime(2023, 1, 20, 10, 30)
        actual = DateHandler.create_date(date_str)
        self.assertEqual(actual, expected)

    def test_validate_date_string_valid_date(self):
        date_strs = ["20/01/2023 10:50",
                     "20/3/2024 17:55"]
        for date_str in date_strs:
            self.assertTrue(Validator.validate(date_str))

    def test_validate_date_string_not_valid_date(self):
        invalid_date_str_list = ["50/01/2023 10:50",
                                 "00/01/2023 10:50",
                                 "5/01 10:50",
                                 "03/02 10:56",
                                 "50/01/2023 44:50"]
        for invalid_date_str in invalid_date_str_list:
            self.assertFalse(Validator.validate(invalid_date_str), f"{invalid_date_str} Failed the Test")
