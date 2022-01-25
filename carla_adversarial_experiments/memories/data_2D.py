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

from distance_calculations.find_features import return_feature_vector
from distance_calculations.pytorch_modified_msssim import ssim, ms_ssim, SSIM, MS_SSIM

sys.path.append("../")
from split_train_test.split_data import get_classwise_file_list

def pre_process(image_path, device):

    # This repetition of the array twice to make it shape like an image
    # is required since otherwise the library complains.

    image = np.asarray(Image.open(image_path))
    image = transforms.ToTensor()(image)
    image.to(device)
    return image


def generate_data():

    data_dictionary = {}
    real_medoids = [0.5, 6, 21, -10]
    radius = [1, 2, 1, 4]

    data_list = {}

    for id in range(1000):

        random_index = random.randint(0, len(real_medoids)-1)

        current_medoid = real_medoids[random_index]
        current_radius = real_medoids[random_index]

        random_number = random.uniform(current_medoid - current_radius, current_medoid + current_radius)
        data_list["n_" + str(id)] = random_number

    return data_list

class data:
    def __init__(self, device):

        self.device = device
        self.raw_image = None
        self.memory_image = None
        self.memory_mask = None
        self.seg_feature = None

        # The actual lesion which serves as memory
        self.lesion_filename = "lesion_memory.png"

        # The interesting mask region
        self.mask_filename = "mask_memory.png"

        # The interesing features
        self.features_filename = "lesion_features.json"


        # Copied from Yahan's tuning of these weight metrics
        self.weight_vector = [0.0, 0.0, 0.05, 0.05, 0.1, 0.4, 0.1, 0.1, 0.2] # Last one is for image
        self.image_weight = 0.3

    def create_data_from_files(self, files_list):
        # The actual lesion image

        self.raw_image = cv2.imread(files_list["image"], cv2.IMREAD_COLOR)
        self.memory_image = pre_process(files_list["image"], self.device)
        self.memory_mask = cv2.imread(files_list["mask"], cv2.IMREAD_GRAYSCALE)
        self.seg_feature = return_feature_vector(files_list["image"], files_list["mask"], files_list["lesion_info"])

    def save_data_as_memory(self, dir_name):
        pass


    def read_data_as_memory(self, dir_name):
        pass

    def compute_disance(self, another_data):

        image_list = [another_data.memory_image]
        feature_list = [another_data.seg_feature]
        torch_image = torch.stack(image_list, dim = 0)

        numpy_image_d = self.compute_image_distance_batched(image_list)
        feature_distance = self.compute_feature_distance_batched(feature_list)

        distance = self.image_weight * numpy_image_d
        distance += feature_distance

        return distance

    def compute_distance_batched(self, other_data_collection):

        # Other data is assumed to be a dictionary mapping from "string" --> < data > type

        if other_data_collection is None :
            return None

        distance_mapping = {}

        # Collect all the images in a tensor, and the single memory image
        index = 0
        image_collection_list = []
        feature_collection = []
        list_index_to_image_name = {}

        for name in other_data_collection.keys():
            current_data = other_data_collection[name]["data"]

            image_collection_list.append(current_data.memory_image)
            feature_collection.append(current_data.seg_feature)

            list_index_to_image_name[index] = name
            index += 1

        image_collection = torch.stack(image_collection_list, dim = 0)
        numpy_image_distance_collection = self.compute_image_distance_batched(image_collection)
        feature_distance_collection = self.compute_feature_distance_batched(feature_collection)

        assert len(feature_distance_collection) == len(numpy_image_distance_collection)

        for index in range(len(feature_distance_collection)):

            name = list_index_to_image_name[index]

            distance = self.image_weight * numpy_image_distance_collection[index]
            distance += feature_distance_collection[index]

            distance_mapping[name] = distance


        assert len(distance_mapping) == len(feature_distance_collection)

        return distance_mapping

    def compute_feature_distance_batched(self, feature_collection):

        result_list = []
        for each_feature in feature_collection:
            distance = 0
            assert len(self.seg_feature) == len(each_feature)
            assert len(self.seg_feature) == len(self.weight_vector)
            for index in range(len(self.seg_feature)):
                distance += self.weight_vector[index] * np.power( self.seg_feature[index] - each_feature[index] , 2.0)

            result_list.append(distance)

        return result_list

    def compute_image_distance_batched(self, collection_of_lesion_images):

        others_count = collection_of_lesion_images.shape[0]

        memory_image_repeated = self.memory_image.repeat([others_count,1,1,1]).to(self.device)
        ssim_val = ssim(memory_image_repeated, collection_of_lesion_images, data_range=1, size_average=False).detach().cpu()

        return ssim_val.numpy()
