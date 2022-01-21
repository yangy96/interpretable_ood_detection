import sys
import json
import matplotlib.pyplot as plt
import os
import numpy as np
import time

def find_crash_prediction(test_file, memorization_object, threshold = 15, interval = 32, prob_threshold = 0.5):

    file = open(test_file)
    time_stamped_lidar = json.load(file)

    ood_interval = 0
    non_ood_interval = 0
    store = []
    for _ in range(interval):
        store.append(0)

    exp_time = []

    # 18/32


    for time_stamp in time_stamped_lidar.keys():
        start_ = time.time()
        nearest_memory, matched_set, probability = memorization_object.find_match(time_stamped_lidar[time_stamp]["trace"])
        
        #print("probability ",probability)
        if probability > prob_threshold:
            ood_interval = 0
            store[int(time_stamp) % interval] = 0
        else:
            ood_interval += 1
            store[int(time_stamp) % interval] = 1
        end_ = time.time()
        exp_time.append(round((end_-start_)*1000,5))
        #print("Execution time in ms", round((end_-start_)*1000,5))
        # print("Store sum - ", sum(store))

        if sum(store) > threshold:
            return True, int(time_stamp), exp_time
    file.close()


    return False, None, exp_time




def find_real_crash_time(test_file):
    file = open(test_file)
    time_stamped_lidar = json.load(file)

    for time_stamp in time_stamped_lidar.keys():
        if int(time_stamped_lidar[time_stamp]["crash"]) == 1:
            return True, int(time_stamp)

    file.close()

    return False, None




def compute_crash_prediction_accuracy(source_dir, memorization_object,window_size, threshold, prob_threshold):
    real_crash_count = 0
    predicted_crash_count = 0

    prediction_matches = 0
    false_predictions = 0
    missed_predictions = 0

    total = 0

    lidar_list = {}

    print("-"*20)
    #print("window size", window_size, " threshold", threshold)

    evaluate_time_list=[]
    alarm_time_list = []
    delay_time_list=[]

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if(file.endswith("json") ):
                file_location = os.path.join(root, file)
                # print("Looking at file - ", file_location)
                
                flag_pred, pred_time, exp_time_list = find_crash_prediction(file_location, memorization_object,threshold = threshold, interval = window_size, prob_threshold=prob_threshold)
                evaluate_time_list.append(exp_time_list)
                
                #flag_real = False
                flag_real, real_time = find_real_crash_time(file_location)
                

                if flag_pred :
                    # print("\t Crash predicted at time --- ", pred_time, end=" ")
                    predicted_crash_count += 1
                else:
                    pass
                    # print("\t No crash predicted.")

                if flag_real :
                    # print("\t Real crash happens at time -- ", real_time)
                    real_crash_count += 1
                else:
                    pass
                    # print("\t No real crash happens.")
                
                if(flag_pred and flag_real and (int(pred_time) >= int(real_time))):
                    delay_time_list.append(int(pred_time)-int(real_time))

                if flag_pred and flag_real and (int(pred_time) < int(real_time)) :
                    #print("Alarm Time ", real_time-pred_time)
                    alarm_time_list.append(real_time-pred_time)
                    prediction_matches += 1
                elif flag_pred and (not flag_real):
                    false_predictions += 1
                elif (not flag_pred) and flag_real:
                    missed_predictions += 1

                total += 1
                # sys.exit()

    results_stat = {}
    #print("Total episode ", total, "Reaf crash total ", real_crash_count)
    results_stat["real_crash_percent"] = np.round(float(real_crash_count / total) * 100.0, 2)
    results_stat["crash_predicted_percent"] = np.round(float(predicted_crash_count / total) * 100.0, 2)
    if real_crash_count > 0:
        results_stat["correct_prediction_percent"] = np.round(float(prediction_matches/real_crash_count) * 100.0, 2)
        if (predicted_crash_count) > 0:
            results_stat["false_predictions"] = np.round(float(false_predictions/predicted_crash_count) * 100.0, 2)
        else:
            results_stat["false_predictions"] = 0
        results_stat["missed_predictions"] = np.round( (float(missed_predictions / real_crash_count)) * 100, 2)
    #results_stat["evaluate_time_list"] = evaluate_time_list
    results_stat["alarm time ahead"] = alarm_time_list
    results_stat["alarm time delay"] = delay_time_list
    #print("correct_prediction_percent ",results_stat["correct_prediction_percent"])
    #print("false_predictions ", results_stat["false_predictions"])
    return results_stat
