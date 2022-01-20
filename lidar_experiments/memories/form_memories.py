import numpy as np
from shutil import copyfile
import json
import matplotlib.pyplot as plt
# sys.path.append("../memories/")
from memories.memorization import memory, memorization
from crash_prediction.predict_crash import compute_crash_prediction_accuracy

import warnings
warnings.filterwarnings("ignore")

def build_memories(source_dir, dest_dir, init_distance):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    memorization_object = memorization(source_dir, dest_dir)
    # memorization_object.learn_memories(0.35)
    memorization_object.learn_memories_with_CLARANS(init_distance_threshold = init_distance)

    # memorization_object.load_memories()


def run_crash_prediction(memory_dir, source_dir, window_size, prob_threshold, window_threshold):

    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.1)
    result_stat ={}
    dist = memory_dir.split("/")[-1].split("_")[-1]
    stats = compute_crash_prediction_accuracy(source_dir, memorization_object,window_size, window_threshold, prob_threshold)
    #print("Stats computed - ", stats)
    print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(window_threshold),str(prob_threshold),str(dist)))
    print("TPR: ",stats["correct_prediction_percent"])
    print("FPR: ",stats["false_predictions"])
    print("MPR: ",stats["missed_predictions"])
    if (len(stats["alarm time ahead"]) > 0):
        print("Avg Forecast: ",round(sum(stats["alarm time ahead"])/len(stats["alarm time ahead"]),2))
    else:
        print("Avg Forecast: N/A")   
    return stats
