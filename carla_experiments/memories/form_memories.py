import os
import numpy as np
import time

from memories.memorization import memory, memorization
from crash_prediction.predict_carla import check_carla_ood, check_carla_heavy_rain_ood
from crash_prediction.predict_crash import compute_crash_prediction_accuracy
import logging

def build_memories_lidar(source_dir, dest_dir, init_distance):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    memorization_object = memorization(source_dir, dest_dir)
    memorization_object.learn_memories_with_CLARANS(init_distance_threshold = init_distance)

def build_memories_carla(source_dir, dest_dir, init_distance):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    memorization_object = memorization(source_dir, dest_dir)
    start_ = time.time()
    memorization_object.learn_memories_with_CLARANS(init_distance_threshold = init_distance)
    end_ = time.time()


def run_crash_prediction(memory_dir, source_dir):


    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.48)

    stats = compute_crash_prediction_accuracy(source_dir, memorization_object)
    return stats

def run_carla_prediction(memory_dir, source_dir, initial_memory_threshold, detect_threshold,prob_threshold,window_size,window_threshold,task):

    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.05)
    if task == "heavy_rain":
        stats = check_carla_heavy_rain_ood(source_dir, memorization_object, initial_memory_threshold, window_size,int(window_threshold),detect_threshold,prob_threshold)
        f = open("./results/carla_"+task+"_exp_results.txt", "a")
        if source_dir.split("/")[-1] == "in_test":
            print("**************************************************************")
            print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
            f.write("(W: {} tau: {} alpha: {} dist: {} ) ".format(str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
            print("FP: %d/%d" %(stats["ood_episode"],stats["total_episode"]))
            f.write("FP: {}/{}" .format(str(stats["ood_episode"]),str(stats["total_episode"])))
        else:
            print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
            f.write("(W: {} tau: {} alpha: {} dist: {} ) ".format(str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
            if(len(stats["detect_frame_list"])>0):
                print("FN: %d/%d Avg Delay: %f Exec Time: %f "%(stats["total_episode"]-stats["ood_episode"],stats["total_episode"],stats["average_window_delay"],stats["average_evaluate_time"]))
                f.write("FN: {}/{} Avg Delay: {} Exec Time: {} \n".format(str(stats["total_episode"]-stats["ood_episode"]),str(stats["total_episode"]),str(stats["average_window_delay"]),str(stats["average_evaluate_time"]) ))
            else:
                print("FN: %d/%d Avg Delay: N/A Exec Time: N/A "%(stats["total_episode"]-stats["ood_episode"],stats["total_episode"]))
                f.write("FN: {}/{} Avg Delay: N/A \n Exec Time: N/A".format(str(stats["total_episode"]-stats["ood_episode"]),str(stats["total_episode"]) ))
                stats["average_window_delay"]=None
        f.close()
    else:
        stats = check_carla_ood(source_dir, memorization_object, initial_memory_threshold, window_size,int(window_threshold),detect_threshold,prob_threshold, task)
        print("**************************************************************")
        f = open("./results/carla_"+task+"_exp_results.txt", "a")
        print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
        f.write("(W: {} tau: {} alpha: {} dist: {} ) ".format(str(window_size),str(window_threshold),str(prob_threshold),str(initial_memory_threshold)))
        if(len(stats["detect_frame_list"])>0):
            print("FN: %d/%d Avg Delay: %f "%(stats["total_episode"]-stats["ood_episode"],stats["total_episode"],sum(stats["window_list"])/len(stats["detect_frame_list"])))
            stats["average_window_delay"]=sum(stats["window_list"])/len(stats["detect_frame_list"])
            f.write("FN: {}/{} Avg Delay: {} \n".format(str(stats["total_episode"]-stats["ood_episode"]),str(stats["total_episode"]),str(sum(stats["window_list"])/len(stats["detect_frame_list"])) ))
        else:
            print("FN: %d/%d Avg Delay: N/A "%(stats["total_episode"]-stats["ood_episode"],stats["total_episode"]))
            f.write("FN: {}/{} Avg Delay: N/A \n".format(str(stats["total_episode"]-stats["ood_episode"]),str(stats["total_episode"]) ))
            stats["average_window_delay"]=None
        f.close()
    return stats

def dump_distances(memory_dir):
    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.05)
    memorization_object.dump_memory_distance(memory_dir)