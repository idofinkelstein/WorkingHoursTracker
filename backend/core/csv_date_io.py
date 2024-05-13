import os
import csv


class IOHandler(object):
    CURR_MODULE_PATH = os.path.dirname(os.path.join(__file__))
    PARENT_DIR, _ = os.path.split(CURR_MODULE_PATH)
    PATHNAME = os.path.join(PARENT_DIR, "resources", "data")
    FILE_NAME = "data.csv"
    FULL_PATH = os.path.join(PATHNAME, FILE_NAME)

    @staticmethod
    def save_to_csv(filename, start_date, end_date, hour_amount):
        headers = ["start_date", "end_date", "hour_amount"]
        file_exist = os.path.exists(filename)
        with open(filename, "a", newline='') as csv_file:
            writer = csv.writer(csv_file)

            if not file_exist:
                writer.writerow(headers)

            writer.writerow([start_date, end_date, hour_amount])

    @staticmethod
    def read_lines_from_csv(csv_file):
        rows = []
        try:
            with open(IOHandler.FULL_PATH, 'r', newline='') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    rows.append(row)
            rows.remove(rows[0])
        except FileNotFoundError as e:
            return rows
        return rows
