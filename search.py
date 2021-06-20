import csv
from pathlib import Path


class Search:

    def __init__(self, input_file, output_headers=None, date_start=None, date_end=None):
        self.input_file = Path(input_file)
        self.input_headers = find_headers(input_file)
        self.output_headers = output_headers # curated headers. [list of indexes??]
        self.date_start = date_start
        self.date_end = date_end

        if self.output_headers is not None:
            self.output_headers_id = [self.input_headers.index(i) for i in self.output_headers]
            self.output_headers_id.sort()


def find_headers(file_path):
    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            while len(row) > 0 and '' not in row[0:]:
                return row