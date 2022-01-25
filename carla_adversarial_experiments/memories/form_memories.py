import os
import numpy as np
import time
# sys.path.append("../memories/")
from memories.memorization import memory, memorization
from crash_prediction.predict_carla import check_carla_crash_ood


np.random.seed(101)

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


def run_carla_prediction(memory_dir, source_dir, initial_memory_threshold,prob_threshold,window_size,win_thre):

    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.05)

    print("**************************************************************")
    print("(W: %s tau: %s alpha: %s dist: %s) " % (str(window_size),str(win_thre),str(prob_threshold),str(initial_memory_threshold)))
    stats = check_carla_crash_ood(source_dir, memorization_object, initial_memory_threshold, window_size,win_thre,prob_threshold)
    f = open("./results/carla_sticker_exp_results.txt", "a")
    f.write("(W: {} tau: {} alpha: {} dist: {} ) ".format(str(window_size),str(win_thre),str(prob_threshold),str(initial_memory_threshold)))
    f.write("Mem: {} ".format(str(len(memorization_object.current_memory_dictionary))))
    print("Mem: %d TPR: %f FPR: %f MPR: %f Avg Forecast: %f" % (len(memorization_object.current_memory_dictionary), stats["corrrect_collision_rate"],stats["wrong_collision_rate"],stats["miss_collision_rate"],stats["early_alarm"]))
    f.write("TPR: {} FPR: {} MPR: {} Avg Forecast: {} \n".format(str(stats["corrrect_collision_rate"]),str(stats["wrong_collision_rate"]),str(stats["miss_collision_rate"]),str(stats["early_alarm"])))
    f.close()
    return stats

def dump_distances(memory_dir):
    memorization_object = memorization(None, memory_dir)
    memorization_object.load_memories(expand_radius = 0.05)
    memorization_object.dump_memory_distance(memory_dir)