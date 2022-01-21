import sys
import json
import matplotlib.pyplot as plt
import os
import numpy as np

def find_crash_prediction(test_file, memorization_object, threshold = 15, interval = 32):

    file = open(test_file)
    time_stamped_lidar = json.load(file)

    ood_interval = 0
    non_ood_interval = 0
    store = []
    for _ in range(interval):
        store.append(0)



    # 18/32


    for time_stamp in time_stamped_lidar.keys():
        nearest_memory, matched_set = memorization_object.find_match(time_stamped_lidar[time_stamp]["trace"])

        if nearest_memory is not None:
            ood_interval = 0
            store[int(time_stamp) % interval] = 0
        else:
            ood_interval += 1
            store[int(time_stamp) % interval] = 1

        # print("Store sum - ", sum(store))

        if sum(store) > threshold:
            return True, int(time_stamp)
    file.close()


    return False, None




def find_real_crash_time(test_file):
    file = open(test_file)
    time_stamped_lidar = json.load(file)

    for time_stamp in time_stamped_lidar.keys():
        if int(time_stamped_lidar[time_stamp]["crash"]) == 1:
            return True, int(time_stamp)

    file.close()

    return False, None




def compute_crash_prediction_accuracy(source_dir, memorization_object):
    real_crash_count = 0
    predicted_crash_count = 0

    prediction_matches = 0
    false_predictions = 0
    missed_predictions = 0

    total = 0

    lidar_list = {}

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if(file.endswith("json") ):
                file_location = os.path.join(root, file)
                # print("Looking at file - ", file_location)

                flag_pred, pred_time = find_crash_prediction(file_location, memorization_object)
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

                if flag_pred and flag_real and (int(pred_time) < int(real_time)) :
                    prediction_matches += 1
                elif flag_pred and (not flag_real):
                    false_predictions += 1
                elif (not flag_pred) and flag_real:
                    missed_predictions += 1

                total += 1
                # sys.exit()

    results_stat = {}
    results_stat["real_crash_percent"] = np.round(float(real_crash_count / total) * 100.0, 2)
    results_stat["crash_predicted_percent"] = np.round(float(predicted_crash_count / total) * 100.0, 2)
    results_stat["correct_prediction_percent"] = np.round(float(prediction_matches/real_crash_count) * 100.0, 2)
    results_stat["false_predictions"] = np.round(float(false_predictions/predicted_crash_count) * 100.0, 2)
    results_stat["missed_predictions"] = np.round( (float(missed_predictions / real_crash_count)) * 100, 2)

    return results_stat


def compute_carla_prediction_accuracy(source_dir, memorization_object):
    real_crash_count = 0
    predicted_crash_count = 0

    prediction_matches = 0
    false_predictions = 0
    missed_predictions = 0

    total = 0

    lidar_list = {}

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if(file.endswith("json") ):
                file_location = os.path.join(root, file)
                # print("Looking at file - ", file_location)

                flag_pred, pred_time = find_crash_prediction(file_location, memorization_object)
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

                if flag_pred and flag_real and (int(pred_time) < int(real_time)) :
                    prediction_matches += 1
                elif flag_pred and (not flag_real):
                    false_predictions += 1
                elif (not flag_pred) and flag_real:
                    missed_predictions += 1

                total += 1
                # sys.exit()

    results_stat = {}
    results_stat["real_crash_percent"] = np.round(float(real_crash_count / total) * 100.0, 2)
    results_stat["crash_predicted_percent"] = np.round(float(predicted_crash_count / total) * 100.0, 2)
    results_stat["correct_prediction_percent"] = np.round(float(prediction_matches/real_crash_count) * 100.0, 2)
    results_stat["false_predictions"] = np.round(float(false_predictions/predicted_crash_count) * 100.0, 2)
    results_stat["missed_predictions"] = np.round( (float(missed_predictions / real_crash_count)) * 100, 2)

    return results_stat