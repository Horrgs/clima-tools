import csv
from pathlib import Path
from enum import Enum


class SearchType(Enum):
    LOCAL_FILE = 1
    NOAA_API = 2


class Search:

    def __init__(self, **kwargs):
        self.search_type = None
        self.local_file = None
        self.path_file = None
        self.curate_options = None
        self.headers = None
        self.output_options = None
        self.input_headers = None

        self.__dict__.update(kwargs)

    def update(self, data):
        for key, value in data.items():
            if key == 'local_file':
                setattr(self, 'path_file', Path(value))
                self.input_headers = find_headers(self.path_file)
            setattr(self, key, value)

    def search(self):
        if self.search_type == SearchType.LOCAL_FILE:
            pass


def find_headers(path_file):
    with open(path_file, 'r') as input_file:
        reader = csv.reader(input_file)
        # fails on .xlsx files (need pandas :( )
        for row in reader:
            while len(row) > 0 and '' not in row[0:]:
                return row

    # indexes = [headers.index(i) for i in heads]
    # this statement can be used to find the index of flagged headers that will be filtered. move upscope not downscope


"""

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
            
            
"""