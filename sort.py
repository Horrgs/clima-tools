import csv
from itertools import groupby
from pathlib import Path


# the file being created is representative of a weather station's data, written to the path specified in argument.
def create_file(path):
    return open(path, mode='w', newline='')


# clean up note
# takes input from GUI and builds the output files. this takes the raw data from a raw data file containing multiple stations and writes them to separate files.
def build(file_path, chunk_size=4096):

    # takes reader of raw data file, break up the raw data file into chunks, allowing faster reading.
    def gen_chunks(reader):
        chunk = []
        for i, line in enumerate(reader):  # create generator for chunks

            if i % chunk_size == 0 and i > 0:  # chunk generation
                yield chunk
                del chunk[:]
            chunk.append(line)

        yield chunk

    output_files = {}  # dict of each station's file descriptor.
    storage = Path(file_path).parent.joinpath('{0}/'.format(file_path.stem))
    storage.mkdir(exist_ok=True)

    # sorts chunks and breaks them up by station ID.
    with open(file_path, 'rt') as input_file:
        reader = csv.reader(input_file)
        headers = next(reader)  # get headers of raw data file so they can be written to each station.
        for sub in gen_chunks(reader):
            for station, measurements in groupby(sub, key=lambda x: x[0]):  # gets first key, station ID
                if station not in output_files:  # check if station's file (descriptor) exists, if not create
                    file = Path(storage).joinpath("{0}.csv".format(station))
                    output_files[station] = create_file(file)
                    csv.writer(output_files[station]).writerow(headers)
                csv.writer(output_files[station]).writerows(measurements)  # write data to station file.

    # close files
    for file in output_files:
        output_files[file].close()