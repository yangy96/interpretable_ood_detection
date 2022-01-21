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
    return int((e.split("/")[-1]).split(".")[0])

def read_image(folder,img_folder):
    img_list = []
    filter_list = []
    #print(folder)
    #print(folder.split("/")[-1])
    for root, dirs, files in os.walk(img_folder):
        for file_ in files:
            if(file_.endswith(".csv")):
                with open(os.path.join(root,file_), newline='') as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=',')
                    for row in csv_reader:
                        temp = row[0].split("/")
                        if("(1)" not in temp[-1] and os.path.exists(os.path.join(root, temp[-1]+".png")) ):
                            img_list.append(os.path.join(root, temp[-1]+".png"))
    img_list.sort(key=myFunc)
    #print(img_list)
    return img_list

def read_image_for_carla(img_folder):
    exp_list = []
    for root, dirs, files in os.walk(img_folder):
        for i in dirs:
            if i not in exp_list:
                exp_list.append(i)
    #print(exp_list)
    return exp_list

def check_carla_ood(exp_folder,memorization_object,initial_memory_threshold, window_size,window_thres,detect_threshold,prob_threshold,task):
    exp_list = read_image_for_carla(exp_folder)
    frame_diff = 0
    total_prep = 0
    total=0
    total_detect = 0
    ood_epi = 0
    total_delay = []
    detect_res_list =[]
    detect_frame_list =[]
    threshold_list={"in":20,"out_precipitation":20,"oods_bike":20,"oods_foggy":0,"oods_night":10}
    for exp_num in tqdm(exp_list):
        #print("Current experiments -- no ", exp_num,exp_folder)
        window = []
        total_exp_time = []
        episode = False
        window_delay = 0
        #mapping img to the memory
        img_list = read_image(exp_folder,"./"+exp_folder+"/"+str(exp_num))

        for img_path in img_list:
            #print("img path ", img_path)
            current_frame = int(img_path.split("/")[-1][:-4])
            total += 1
            key = img_path.split("/")[-2]+"/"+img_path.split("/")[-1]
            start_ = time.time()
            nearest_memory, matched_set, prob_density, exp_time_ = memorization_object.find_match(img_path,initial_memory_threshold)
            #(key,nearest_memory,matched_set)
            if (len(window) >= window_size):
                window.pop(0)
                if (prob_density < prob_threshold):
                    window.append(0)
                else:
                    window.append(1)
                total_win = window.count(0)
                if (total_win >= window_thres and episode == False):
                    episode = True
                    total_detect += 1
                    detect_frame_list.append(current_frame)
                    #print("detection at: ",current_frame)
                    
            else:
                if (prob_density < prob_threshold):
                    window.append(0)
                else:
                    window.append(1)

            #test ood episode for only
            total_exp_time.append(round((time.time()-start_)*1000,2)) 

            if(episode == True):
                break
        detect_res_list.append(episode)
        total_delay.append(window_delay)
        if (episode):
            ood_epi += 1

    results_stat = {}
    #print("**************************************************************")
    #print("Current window size: ",window_size," window threshold: ",window_thres)
    #print("total number of ood episode",ood_epi," total episode",len(exp_list))
    
    #if (total_detect > 0):
    #    print("frame_diff ", frame_diff/total_detect, "stop prepcipitation ", total_prep/total_detect)
    #else:
    #    print("frame_diff ", 0, "stop prepcipitation ", 0)
    
    results_stat["detection_rate"] = round(ood_epi/len(exp_list),3)
    results_stat["ood_episode"] = ood_epi
    results_stat["total_episode"] = len(exp_list)
    results_stat["detect_frame_list"] = detect_frame_list
    results_stat["detect_res_list"] = detect_res_list
    new_frame=[]
    for m in results_stat["detect_frame_list"]:
        if m > threshold_list[task]:
            new_frame.append(m-threshold_list[task])
        else:
            new_frame.append(0)
    results_stat["window_list"] = new_frame

    return results_stat

