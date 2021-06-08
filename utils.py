import csv
from itertools import groupby
from pathlib import Path
from os.path import exists


def build(file_path, chunk_size=100):
    file_path = Path(file_path.replace("\\", "/")) # .replace to handle unix/windows support
    curate(file_path, chunk_size)


def create_file(path):
    return open(path, mode='w', newline='')


def curate(file_path, chunk_size=100):
    reader = csv.reader(open(file_path, 'rt'))  # start reading file. This may keep file open forever??
    headers = next(reader)

    def gen_chunks():
        chunk = []

        for i, line in enumerate(reader):  # create generator for chunks

            if i % chunk_size == 0 and i > 0:  # chunk generation
                yield chunk
                del chunk[:]
            chunk.append(line)

        yield chunk

    output_files = {}
    storage = Path(file_path).parent.joinpath('curated/')  # folder for curation
    if not storage.exists():
        storage.mkdir()

    # sorts chunks and breaks them up by station ID.
    for sub in gen_chunks():
        for station, measurements in groupby(sub, key=lambda x: x[0]):  # gets first key, station ID
            file = Path(storage).joinpath("{0}.csv".format(station))
            if not exists(file):
                output_files[station] = create_file(file)
                csv.writer(output_files[station]).writerow(headers)
            csv.writer(output_files[station]).writerows(measurements)

    for file in output_files:
        output_files[file].close()


build('test_data.csv', 100)
