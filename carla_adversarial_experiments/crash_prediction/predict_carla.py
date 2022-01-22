import sys
import json
import matplotlib.pyplot as plt
import os
import numpy as np
import random
import csv
import time
from tqdm import tqdm

random.seed(201)

def myFunc(e):
    return int( (e.split("/")[-1]).split(".")[0].split("_")[1] )

def read_image(folder,img_folder):
    img_list = []

    for root, dirs, files in os.walk(img_folder):
        for file_ in files:
            if(file_.endswith(".png")):
                img_list.append(os.path.join(root,file_))
    img_list.sort(key=myFunc)

    return img_list

def read_crash(folder,exp_name):
    with open("./"+folder+"/"+exp_name+'/measurements.csv', newline='') as csvfile:
        frame = 0
        collision = False
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            frame += 1
            if (float(row[1]) > 0.1):
                collision = True
                break
    csvfile.close()
    return frame,collision

def read_image_for_carla(img_folder):
    exp_list = []
    for item in os.listdir(img_folder):
        if item not in exp_list:
            exp_list.append(item)

    return exp_list

def check_carla_crash_ood(exp_folder,memorization_object,initial_memory_threshold, window_size,window_thres,prob_threshold):
    exp_list = read_image_for_carla(exp_folder)
    exp_crash_dict={}
    collision_total = 0
    collision_predict = 0
    correct_collision = 0
    wrong_collision = 0
    late_collision = 0
    miss_collision = 0
    early_alarm = 0

    evaluate_time_list =[]
    detect_pre_list ={}
    detect_delay_list ={}
    close_memory_for_ood={}
    
    for exp_name in tqdm(exp_list):
        window = []
        exp_time = []
        episode = False
        current_frame = 0
        memory_store = []
        #mapping img to the memory
        img_list = read_image(exp_folder,"./"+exp_folder+"/"+str(exp_name))
        frame,collision=read_crash(exp_folder,exp_name)
        exp_crash_dict[exp_name] = {"frame":frame,"collision":collision}

        if (collision):
            collision_total += 1
        for img_path in img_list:
            current_frame += 1

            nearest_memory, matched_set, prob_density, exp_time_ = memorization_object.find_match(img_path,initial_memory_threshold)

            exp_time.append(round((exp_time_)*1000,5))

            if (len(window) >= window_size):
                window.pop(0)
                memory_store.pop(0)
                if (prob_density < prob_threshold):
                    window.append(0)
                else:
                    window.append(1)
                memory_store.append([img_path,nearest_memory])
                total_win = window.count(0)
                if (total_win >= window_thres and episode == False):
                    episode = True
                    collision_predict += 1
                    if (collision and current_frame <= frame):
                        correct_collision += 1
                        detect_pre_list[exp_name] = frame - current_frame
                        
                        early_alarm += frame - current_frame
                    if (collision and current_frame > frame):
                        late_collision += 1
                        detect_delay_list[exp_name] = current_frame - frame

                    if not collision:
                        wrong_collision += 1      
                    
            else:
                memory_store.append([img_path,nearest_memory])
                if (prob_density < prob_threshold):
                    window.append(0)
                else:
                    window.append(1)

            assert(len(window) <= window_size)
            #test ood episode for only
            if(episode == True):
                break
            
        evaluate_time_list.append(exp_time)
        close_memory_for_ood[exp_name] = memory_store
        if (episode == False and collision == True):
            miss_collision += 1

    results_stat = {}
    
    if collision_predict > 0:
        results_stat["corrrect_collision_rate"] = 100*round(correct_collision/collision_total,3)
        results_stat["total_collision_rate"] = 100*round(correct_collision+late_collision/collision_predict,3)
        results_stat["miss_collision_rate"] = 100*round(miss_collision/collision_total,3)
        results_stat["wrong_collision_rate"] = 100*round(wrong_collision/collision_predict,3)
        results_stat["late_collision_rate"] = 100*round(late_collision/collision_predict,3)
        results_stat["early_alarm"]= round(early_alarm/correct_collision,2)
    else:
        results_stat["corrrect_collision_rate"] = 0.0
        results_stat["total_collision_rate"] = 0.0
        results_stat["miss_collision_rate"] = round(miss_collision/collision_total,2)
        results_stat["wrong_collision_rate"] = 0.0
        results_stat["late_collision_rate"] = 0.0
        results_stat["early_alarm"] = 0.0

    return results_stat

