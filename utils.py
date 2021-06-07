import csv
from itertools import groupby
import os

headers = []
curated = {}
chunks = []


def build(file_path, chunk_size=100):
    file_path = file_path.replace("/", "\\")  # windows specific, need to handle Unix/Linux.

    curate(file_path, chunk_size)
    write_files(file_path, curated)


def curate(file_path, chunk_size=100):

    def gen_chunks():
        reader = csv.reader(open(file_path, 'rt'))  # start reading file
        chunk = []

        for i, line in enumerate(reader):  # create generator for chunks
            if i >= 1:  # this should skip the first line
                if i % chunk_size == 0 and i > 0:  # chunk generation
                    yield chunk
                    chunk = []
                chunk.append(line)
            else:
                headers.append(line)
                print(headers)
        yield chunk

    # sorts chunks and breaks them up by station ID.

    for sub in gen_chunks():
        chunks.append(sub)
        for k, v in groupby(sub, key=lambda x: x[0]):  # gets first key, station ID
            if k not in curated:  # if station doesn't exist, add and append.
                curated[k] = list(v)
            else:
                curated[k].append(list(v))  # station exists, just appending


def write_files(file_path, data_set):
    path = (''.join(file_path.rpartition('\\')[:-1]) + "sorted\\")
    print("path {0}".format(path))
    if not os.path.exists(path):
        os.makedirs(path)
        print("Created folder sorted at path {0}".format(path))

    for station in data_set:
        with open("{0}\\{1}.csv".format(path, station), 'w', newline="") as station_file:
            # print("Creating file for station {0} at {1}".format(station, path))
            wr = csv.writer(station_file)
            data_set[station].insert(0, headers[0])
            wr.writerows(data_set[station])


print("Headers are: {0}".format(headers))