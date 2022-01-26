import json
import os
import matplotlib.pyplot as plt
import numpy as np

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
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_lidar_true_prediction_alpha_"+str(prob)+"_d_"+str(dist)+".png",bbox_inches='tight')
    plt.close() 
    plt.figure()

    plt.xticks(np.arange(0, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(keys,false_prediction, label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_lidar_false_prediction_alpha_"+str(prob)+"_d_"+str(dist)+".png",bbox_inches='tight')
    plt.close() 

def plot_ablation():
    window_size = 40
    prob_list = [0.05,0.1,0.15,0.2,0.25,0.3]
    dist_list = [0.2,0.3]

    window_thre_list = range(5,window_size,2)
    correct_prediction={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    false_prediction={dist:{prob: [] for prob in prob_list} for dist in dist_list}
    keys = window_thre_list
    for dist in dist_list:
        for prob in prob_list:
            for i in window_thre_list:
                file_name = "./ood_result"+"_LIDAR_memories_"+str(dist)+"_"+str(window_size)+"_"+str(prob)+"_"+str(i)+".json"
                with open(os.path.join("results",file_name)) as json_file:
                    data = json.load(json_file)
                    correct_prediction[dist][prob].append(data["correct_prediction_percent"])
                    false_prediction[dist][prob].append(data["false_predictions"])        
                json_file.close()
    fig = plt.figure()
    for dist in dist_list:
        for prob in prob_list:
            plt.plot(keys,correct_prediction[dist][prob], label="d: "+str(dist)+" "+"alpha "+str(prob))

    plt.xticks(np.arange(5, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.legend(fontsize=10)
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_lidar_true_prediction.png",bbox_inches='tight')
    plt.close() 

    plt.figure()
    for dist in dist_list:
        for prob in prob_list:
            plt.plot(keys,false_prediction[dist][prob], label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.xticks(np.arange(5, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.legend(fontsize=10)
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_lidar_false_prediction.png",bbox_inches='tight')
    plt.close() 
