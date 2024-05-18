import re
from re import Match


class Validator(object):
    pattern = (r"^(((0?[1-9]|[12][0-9]|3[01])\/(0?[1-9]|1[0-2])\/\d{4})"
               r"|\d{4}-\d{2}-\d{2}) (?:[01]?[0-9]|2[0-3]):[0-5]?[0-9]$")
    matcher = re.compile(pattern)

    @staticmethod
    def validate(date_string: str) -> Match[str] | None:
        return Validator.matcher.match(date_string)

    @staticmethod
    def validate_input(start_date: str, end_date: str) -> bool:
        if Validator.matcher.match(start_date) and Validator.matcher.match(end_date):
            return True
        return False
