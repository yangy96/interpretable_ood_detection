import json
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.xticks(fontsize=20)


def plot_one_result(memory_dir,window_size,dist,prob):
    window_thre_list = range(5,window_size,2)
    correct_prediction=[]
    false_prediction=[]
    miss_prediction=[]
    keys = []

    for i in window_thre_list:
        file_name = "./ood_result"+"_"+memory_dir.split("/")[-1]+"_"+str(window_size)+"_"+str(prob)+"_"+str(i)+".json"
        with open(os.path.join("results",file_name)) as json_file:
            data = json.load(json_file)
            correct_prediction.append(data["correct_prediction_percent"])
            false_prediction.append(data["false_predictions"])
            miss_prediction.append(["missed_predictions"]) 
            keys.append(i)         
        json_file.close()
    fig = plt.figure()
    plt.xticks(np.arange(0, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(keys,correct_prediction, label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.legend(fontsize=10)
    #plt.title("correct prediction rate versus threshold/window")
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_correct_prediction_lidar_(10.a).png",bbox_inches='tight')
    plt.close() 
    plt.figure()

    plt.xticks(np.arange(0, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(keys,false_prediction, label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.legend(fontsize=10)
    #plt.title("false prediction rate versus threshold/window")
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_false_prediction_lidar_(10.b).png",bbox_inches='tight')
    plt.close() 

def plot_saved_ablation_result():
    window_list = [40]
    prob_list = [0.05,0.1,0.15,0.2,0.25,0.3]
    dist_list = [0.2,0.3]

    correct_prediction={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    false_prediction={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    miss_prediction={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    alarm_time ={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    index=[]
    keys = []
    for dist in dist_list:
        for prob in prob_list:
            for i in window_list:
                keys=[]
                file_name = "memory_generation_LIDAR_memories_"+str(dist)+"_"+str(i)+"_"+str(prob)+"_"+str()+".json"
                with open(os.path.join("final_output",file_name)) as json_file:
                    data = json.load(json_file)
                    for p in data.keys():
                        keys.append(str(p))
                        print("***********************************")
                        print("current key ",p)
                        print("correct prediction percent ",data[p]["correct_prediction_percent"])
                        print("false predictions ",data[p]["false_predictions"])
                        print("missed predictions ",data[p]["missed_predictions"])
                        correct_prediction[dist][prob].append(data[p]["correct_prediction_percent"])
                        false_prediction[dist][prob].append(data[p]["false_predictions"])
                        miss_prediction[dist][prob].append(data[p]["missed_predictions"])

                        if (len(data[p]["alarm time ahead"]) > 0):
                            #alarm_time.append(round(sum(data[p]["alarm time ahead"])/len(data[p]["alarm time ahead"]),2))
                            print("average alarm ",sum(data[p]["alarm time ahead"])/len(data[p]["alarm time ahead"]))
                        else:
                            #alarm_time.append(0.0)
                            print("average alarm N/A")            
                json_file.close()

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) 
    for dist in [0.2, 0.3]:
        for prob in prob_list:
            plt.xticks(np.arange(0, 41, 4.0))
            plt.xticks(fontsize=18,weight="bold")
            plt.yticks(fontsize=18,weight="bold")
            plt.plot(keys,correct_prediction[dist][prob], label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.legend(fontsize=10)
    #plt.title("correct prediction rate versus threshold/window")
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("p_correct_prediction_lidar_full_abalation.png",bbox_inches='tight')
    plt.close() 
    plt.figure()
    for dist in [0.2, 0.3]:
        for prob in prob_list:
            plt.xticks(np.arange(0, 41, 4.0))
            plt.xticks(fontsize=18,weight="bold")
            plt.yticks(fontsize=18,weight="bold")
            plt.plot(keys,false_prediction[dist][prob], label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.legend(fontsize=10)
    #plt.title("false prediction rate versus threshold/window")
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("p_false_prediction_lidar_full_abalation.png",bbox_inches='tight')
    plt.close() 
