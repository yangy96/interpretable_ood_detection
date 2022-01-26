#
# Code written by : Souradeep Dutta,
#  duttaso@seas.upenn.edu, souradeep.dutta@colorado.edu
# Website : https://sites.google.com/site/duttasouradeep39/
#

import os
import json
import numpy as np
from shutil import copyfile
import torch
import matplotlib.pyplot as plt
from copy import deepcopy as dc

from distance_calculations.find_features import return_feature_vector
from distance_calculations.pytorch_modified_msssim import ssim, ms_ssim, SSIM, MS_SSIM

max_memories = 10000

def pre_process_lidar(raw_scan):

    # This repetition of the array twice to make it shape like an image
    # is required since otherwise the library complains.


    doubled_lidar_scan = [raw_scan, raw_scan]
    numpy_array = np.asarray(doubled_lidar_scan)
    # Adding 2 pointless dimensions
    for i in range(1):
        numpy_array = np.expand_dims(numpy_array, axis = 0)

    lidar_tensor = torch.from_numpy(numpy_array)

    return lidar_tensor


class data:
    def __init__(self, device):

        self.device = device
        self.lidar_raw = None
        self.lidar_tensor = None

        # The actual lidar which serves as memory
        self.lidar_filename = "lidar_memory.json"



    def create_data_from_scan(self, lidar_scan):
        # The actual lesion image

        self.lidar_raw = dc(lidar_scan)
        self.lidar_tensor = pre_process_lidar(lidar_scan)

    def save_data_as_memory(self, dir_name):

        assert self.lidar_raw is not None
        fp = open(os.path.join(dir_name, self.lidar_filename), "w")
        json.dump(self.lidar_raw, fp)
        fp.close()



    def read_data_as_memory(self, dir_name):

        fp = open(os.path.join(dir_name, self.lidar_filename), "r")
        self.lidar_raw = json.load(fp)
        self.lidar_tensor = pre_process_lidar(self.lidar_raw)
        fp.close()


    def compute_disance(self, another_data):

        lidar_list = [another_data.lidar_tensor]

        torch_lidar = torch.stack(lidar_list, dim = 0)

        numpy_lidar_d = self.compute_image_distance_batched(torch_lidar)

        distance = numpy_lidar_d

        return distance

    def compute_distance_batched(self, other_data_collection):

        # Other data is assumed to be a dictionary mapping from "string" --> < data > type

        if other_data_collection is None :
            return None

        distance_mapping = {}

        # Collect all the images in a tensor, and the single memory image
        index = 0
        lidar_collection_list = []
        list_index_to_lidar_name = {}

        for name in other_data_collection.keys():
            current_data = other_data_collection[name]["data"]
            lidar_collection_list.append(current_data.lidar_tensor)
            list_index_to_lidar_name[index] = name
            index += 1

        lidar_collection = torch.stack(lidar_collection_list, dim = 0)
        numpy_lidar_distance_collection = self.compute_lidar_distance_batched(lidar_collection)

        for index in range(len(numpy_lidar_distance_collection)):
            name = list_index_to_lidar_name[index]
            distance = numpy_lidar_distance_collection[index]
            distance_mapping[name] = distance


        assert len(distance_mapping) == len(numpy_lidar_distance_collection)

        return distance_mapping


    def compute_lidar_distance_batched(self, collection_of_lidar_images):

        others_count = collection_of_lidar_images.shape[0]
        ssim_values_collection = []

        for split in range(0, others_count, max_memories):

            if (others_count - split < max_memories):
                end_idx = others_count
            else:
                end_idx = split + max_memories

            x_list = collection_of_lidar_images[split : end_idx, :]
            x_list = x_list.to(self.device)


            lidar_memory_repeated = self.lidar_tensor.repeat([end_idx - split ,1,1,1]).to(self.device)
            ssim_val = ssim(lidar_memory_repeated, x_list, data_range=1, size_average=False).detach().cpu()
            ssim_values_collection.extend(ssim_val.numpy()[:])

        return ssim_values_collection
