#
# Code written by : Souradeep Dutta,
#  duttaso@seas.upenn.edu, souradeep.dutta@colorado.edu
# Website : https://sites.google.com/site/duttasouradeep39/
#

import os
import json
import numpy as np
from shutil import copyfile
import copy
import random
import torch
import time
import sys
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms, datasets
from copy import deepcopy as dc

from distance_calculations.calculate_distance import compute_distance
from distance_calculations.find_features import return_feature_vector
from distance_calculations.pytorch_modified_msssim import ssim, ms_ssim, SSIM, MS_SSIM

max_memories = 1000

def pre_process_carla(carla_path,device):

    # This repetition of the array twice to make it shape like an image
    # is required since otherwise the library complains.

    transform = transforms.ToTensor()
    carla_tensor = transform(Image.open(carla_path).convert('RGBA').resize((128,128)))
    carla_tensor = carla_tensor.to(device)


    return carla_tensor


class carla_data:
    def __init__(self, device):

        self.device = device
        self.carla_raw = None
        self.carla_tensor = None

        # The actual carla which serves as memory
        self.carla_filename = "carla_memory.json"



    def create_data_from_scan(self, carla_path):
        # The actual lesion image

        self.carla_raw = carla_path
        self.carla_tensor = pre_process_carla(carla_path,self.device)

    def save_data_as_memory(self, dir_name):

        assert self.carla_raw is not None
        fp = open(os.path.join(dir_name, self.carla_filename), "w")
        json.dump(self.carla_raw, fp)
        fp.close()



    def read_data_as_memory(self, dir_name):

        fp = open(os.path.join(dir_name, self.carla_filename), "r")
        self.carla_raw = json.load(fp)
        self.carla_raw = "training_data"+os.sep +self.carla_raw.split("/")[-3]+os.sep+self.carla_raw.split("/")[-2]+os.sep+self.carla_raw.split("/")[-1]
        self.carla_tensor = pre_process_carla(self.carla_raw,self.device)
        fp.close()


    def compute_disance(self, another_data):

        carla_list = [another_data.carla_tensor]

        torch_carla = torch.stack(carla_list, dim = 0)

        numpy_carla_d = self.compute_image_distance_batched(torch_carla)

        distance = numpy_carla_d

        return distance

    def compute_distance_batched(self, other_data_collection):

        # Other data is assumed to be a dictionary mapping from "string" --> < data > type

        if other_data_collection is None :
            return None

        distance_mapping = {}

        # Collect all the images in a tensor, and the single memory image
        index = 0
        carla_collection_list = []
        list_index_to_carla_name = {}

        for name in other_data_collection.keys():
            current_data = other_data_collection[name]["data"]
            carla_collection_list.append(current_data.carla_tensor)
            list_index_to_carla_name[index] = name
            index += 1

        carla_collection = torch.stack(carla_collection_list, dim = 0)
        numpy_carla_distance_collection = self.compute_carla_distance_batched(carla_collection)

        for index in range(len(numpy_carla_distance_collection)):
            name = list_index_to_carla_name[index]
            distance = numpy_carla_distance_collection[index]
            distance_mapping[name] = distance


        assert len(distance_mapping) == len(numpy_carla_distance_collection)

        return distance_mapping


    def compute_carla_distance_batched(self, collection_of_carla_images):

        others_count = collection_of_carla_images.shape[0]
        

        for split in range(0, others_count, max_memories):

            if (others_count - split < max_memories):
                end_idx = others_count
            else:
                end_idx = split + max_memories

            x_list = collection_of_carla_images[split : end_idx, :]
            
            x_list = x_list.to(self.device)

            carla_memory_repeated = self.carla_tensor.repeat([end_idx - split ,1,1,1]).to(self.device)
            
            ssim_val = ssim(carla_memory_repeated, x_list, data_range=1, size_average=False).detach().cpu()
            if (split == 0):
                ssim_val_total = ssim_val.numpy()
            else:
                ssim_val_total = np.concatenate((ssim_val_total, ssim_val.numpy()), axis=0)

        return ssim_val_total
