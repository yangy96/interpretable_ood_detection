import numpy as np
from shutil import copyfile
import json
import matplotlib.pyplot as plt
from memories.memorization import memory, memorization
from crash_prediction.predict_crash import compute_crash_prediction_accuracy
import os
import warnings
warnings.filterwarnings("ignore")

def build_memories(source_dir, dest_dir, init_distance):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    memorization_object = memorization(source_dir, dest_dir)
    memorization_object.learn_memories_with_CLARANS(init_distance_threshold = init_distance)



def run_crash_prediction(memory_dir, source_dir, window_size, prob_threshold, window_threshold):

    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.1)

    dist = memory_dir.split("/")[-1].split("_")[-1]
    stats = compute_crash_prediction_accuracy(source_dir, memorization_object,window_size, window_threshold, prob_threshold)

    f = open("./results/lidar_exp_results.txt", "a")
    print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(window_threshold),str(prob_threshold),str(dist)))
    f.write("(W: {} tau: {} alpha: {} dist: {} ) \n".format(str(window_size),str(window_threshold),str(prob_threshold),str(dist)))
    
    if (len(stats["alarm time ahead"]) > 0):
        print(("TPR: %f FPR: %f MPR: %f Avg Forecast: %f ") %( stats["correct_prediction_percent"], stats["false_predictions"] ,stats["missed_predictions"],round(sum(stats["alarm time ahead"])/len(stats["alarm time ahead"]),2)))
        f.write("TPR: {} FPR: {} MPR: {} Avg Forecast: {} \n".format(str(stats["correct_prediction_percent"]), str(stats["false_predictions"]),str(stats["missed_predictions"]),str(round(sum(stats["alarm time ahead"])/len(stats["alarm time ahead"]),2))))
    else:
        print(("TPR: %f FPR: %f MPR: %f Avg Forecast: N/A ") %( stats["correct_prediction_percent"], stats["false_predictions"] ,stats["missed_predictions"])) 
        f.write("TPR: {} FPR: {} MPR: {} Avg Forecast: N/A \n".format(str(stats["correct_prediction_percent"]), str(stats["false_predictions"]),str(stats["missed_predictions"])))
    
    f.close()  
    return stats
