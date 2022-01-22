import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)



def plot_one_result(memory_dir,window_size,dist,window_threshold):
    prob_list=[0.05,0.1,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
    correct_prediction = []
    false_prediction=[]
    for prob in prob_list:
        in_file = "./ood_result"+"_"+memory_dir.split("/")[-1]+"_"+str(window_size)+"_"+str(prob)+"_"+str(window_threshold)+".json"
        with open(os.path.join("results",in_file)) as json_file:
            data = json.load(json_file)
            correct_prediction.append(data["corrrect_collision_rate"])
            false_prediction.append(data["wrong_collision_rate"])
        json_file.close()

    plt.figure()

    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(prob_list,correct_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window_size))
    plt.legend(fontsize=12)
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_correct_prediction_carla_sticker(6.a).png",bbox_inches='tight')
    plt.close() 

    plt.figure()
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(prob_list,false_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window_size))
    plt.legend(fontsize=12)
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_false_prediction__carla_sticker(6.b).png",bbox_inches='tight')
    plt.close() 