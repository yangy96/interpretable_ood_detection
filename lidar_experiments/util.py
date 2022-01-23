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
    plt.savefig("./results/p_lidar_true_prediction_alpha_"+prob+"_d_"+dist+".png",bbox_inches='tight')
    plt.close() 
    plt.figure()

    plt.xticks(np.arange(0, 41, 4.0))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(keys,false_prediction, label="d: "+str(dist)+" "+"alpha "+str(prob))
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Threshold/Window",fontsize=18,weight="bold")
    plt.savefig("./results/p_lidar_false_prediction_alpha_"+prob+"_d_"+dist+".png",bbox_inches='tight')
    plt.close() 
