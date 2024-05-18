from datetime import datetime, timedelta


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

    @staticmethod
    def construct_timedelta_from_string(timedelta_string: str):

        def handle_time_parts(time_string: str):
            duration_parts = time_string.split(":")
            return timedelta(hours=int(duration_parts[0]),
                             minutes=int(duration_parts[1]),
                             seconds=int(duration_parts[2]))

        parts = timedelta_string.split(',')
        time_delta = timedelta()

        if len(parts) > 1:

            value, unit = parts[0].split()
            time_duration = handle_time_parts(parts[1])
            try:
                value = int(value)
            except ValueError:
                return None
            if unit == "day" or "days":
                time_delta += timedelta(days=value) + time_duration
            else:
                return None
        else:
            time_duration = handle_time_parts(parts[-1])
            time_delta += time_duration
        return time_delta


