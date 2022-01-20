import csv
import sys
import os
import json


def read_file(filename = '../hscc20_data_traces/uncovered/DDPG_L21_64x64_Controller1/run1.csv'):

    time_stamped_lidar = {}
    start = 2 + 20 * 4 - 1
    end = 1084 - 4 * 20 + 1
    delta = int(11.5 * 4)

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        id = 0
        for row in readCSV:
            time_stamped_lidar[id] = {}
            time_stamped_lidar[id]["trace"] = []
            current_index = start
            while current_index <= end :
                dist = min(float(row[current_index]), 5.0)
                time_stamped_lidar[id]["trace"].append(dist)
                current_index += delta

            time_stamped_lidar[id]["crash"] = row[-1]
            id += 1
    return time_stamped_lidar


def read_and_write(src_dir, real_dest_dir):

    for root, subdirs, files in os.walk(src_dir):
        if "Controller" in root :
            current_sub_dir = os.path.split(root)[1]

            dest_dir = os.path.join(real_dest_dir, current_sub_dir)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for file in files :
                filename = os.path.join(root, file)

                index = file.find(".csv")
                destination_file = file[:index] + ".json"
                destination_file = os.path.join(dest_dir, destination_file)

                print("Reading File - ", filename, " writing to file - ", destination_file)

                trace_data = read_file(filename)
                with open(destination_file, 'w') as outfile:
                    json.dump(trace_data, outfile, indent = 2)


# real_data_dir_modified = "../hscc20_data_traces/covered/"
# real_data_destination = "./modified/"
# read_and_write(real_data_dir_modified, real_data_destination)

real_data_dir_modified = "../hscc20_data_traces/uncovered/"
real_data_destination = "./unmodified/"
read_and_write(real_data_dir_modified, real_data_destination)
