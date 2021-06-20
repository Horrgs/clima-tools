import csv
from search import Search


# reads file in chunks, allowing faster reading.
def gen_chunks(reader, chunk_size=4096):
    chunk = []
    for i, line in enumerate(reader):  # create generator for chunks

        if i % chunk_size == 0 and i > 0:  # chunk generation
            yield chunk
            del chunk[:]
        chunk.append(line)

    yield chunk


# find headers of a CSV file.
def find_headers(path_file):
    with open(path_file, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            while len(row) > 0 and '' not in row[0:]:
                return row

    # indexes = [headers.index(i) for i in heads]
    # this statement can be used to find the index of flagged headers that will be filtered. move upscope not downscope


"""
input - [['1', 3, 5], ['', 2, 9]]

Output format:
[total, days, [total_entries]]
total - [1, 5, 14] - counts the total of each measurement.
days - [1, 2, 2] - counts the total days for each measurement (so after measuring)
total_entries [2] - counts the total amount of days in data set *being measured.*

"""

#
def get_data_for_columns(data, search: Search):
    if search.output_headers is not None:  # needs to be kept for now until we figure out alphabetic columns. yikes.
        curated = [list(row[header_id] for row in data) for header_id in search.output_headers_id]  # filters out unneedeed headers and rearranges lists into index.
        curated = [list(map(float, filter(None, sublist))) for sublist in curated]  # filters out blankspace & cast floats

        total = [sum(sublist) for sublist in curated]  # sums each sublist (header)
        days = [len(sublist) for sublist in curated]  # counts days of each sublist.
        total_days = len(data)  # counts total days of measurement.
        return [total, days, [total_days]]


# takes two lists that are outputted from get_data_columns and combines them in the same output.
def sum_lists(a, b):
    output = []
    for a, b in zip(a, b):
        output.append([sum(x) for x in zip(*[a, b])])
    return output


"""
inp = [[0, 445.79999999999995], [0, 31], [31]]

list_a = takes item in list_a and divides by same index in list b (total / total_days of each measurement)
list_b = unchanged, see other notes.
list_c = unchanged.
list_d = measures data accuracy for each measurement for month.
Output:
oup = [[0, 14.38], [0, 31], [31], [0%, 100%]] 
"""

def curate_list(input_list):
    lst_a = [a / b for a, b in zip(input_list[0], input_list[1])]
    val = input_list[2][0]
    lst_d = [input_list[1][i] / val for i in range(len(input_list[1]))]
    return [lst_a, input_list[1], input_list[2], lst_d]
