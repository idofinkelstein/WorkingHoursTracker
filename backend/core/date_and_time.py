"""
In this module I want to implement the following:
A class that implements calculate method for calculating subtract 2 dates.
"""


from datetime import datetime


class DateHandler(object):

    @staticmethod
    def subtract_time(start_date: datetime, end_date: datetime):
        try:
            return end_date - start_date
        except TypeError as e:
            print(e)

    @staticmethod
    def create_date(date_str: str) -> datetime:
        # string format: "dd/MM/yyyy HH:mm"
        date_part = None
        time_part = None
        try:
            all_parts = date_str.split(" ")
            date_part, time_part = all_parts[0], all_parts[1]
            date_parts = date_part.split("/")
            time_parts = time_part.split(":")
            return datetime(day=int(date_parts[0]),
                            month=int(date_parts[1]),
                            year=int(date_parts[2]),
                            hour=int(time_parts[0]),
                            minute=int(time_parts[1]))
        except ValueError as e:
            print(e)
