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
        in_file = "ood_result_adv"+"_"+str(dist)+"_"+str(window_size)+"_"+str(prob)+"_"+str(window_threshold)+".json"
        with open(os.path.join("results",in_file)) as json_file:
            data = json.load(json_file)
            #load TPR and FPR from json file
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
    plt.savefig("./results/p_sticker_true_prediction_T_"+str(window_threshold)+"_W_"+str(window_size)+"_d_"+str(dist)+".png",bbox_inches='tight')
    plt.close() 

    plt.figure()
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    plt.plot(prob_list,false_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window_size))
    plt.legend(fontsize=12)
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_sticker_false_prediction_T_"+str(window_threshold)+"_W_"+str(window_size)+"_d_"+str(dist)+".png",bbox_inches='tight')
    plt.close() 

def plot_abalation():
    prob_list=[0.05,0.1,0.2,0.25,0.3,0.35,0.4,0.45,0.5]
    win_thre = [5,5,7,9]
    window_size=[5,10,10,10]
    dist_list=[0.5,0.6]

    correct_prediction={dist:{str(m)+"/"+str(n): [] for m,n in zip(win_thre,window_size)} for dist in dist_list}
    false_prediction={dist:{str(m)+"/"+str(n): [] for m,n in zip(win_thre,window_size)} for dist in dist_list}
    
    
    for dist in dist_list:
        for win_thre,win_size in zip(win_thre,window_size):
            for prob in prob_list:
                in_file = "ood_result_adv"+"_"+str(dist)+"_"+str(win_size)+"_"+str(prob)+"_"+str(win_thre)+".json"
                with open(os.path.join("results",in_file)) as json_file:
                    data = json.load(json_file)
                    #load TPR and FPR from json file
                    correct_prediction[dist][str(win_thre)+"/"+str(win_size)].append(data["corrrect_collision_rate"])
                    false_prediction[dist][str(win_thre)+"/"+str(win_size)].append(data["wrong_collision_rate"])
                json_file.close()

    plt.figure()

    for dist in dist_list:
        for win_thre,win_size in zip(win_thre,window_size):
            plt.plot(prob_list,correct_prediction[dist][str(win_thre)+"/"+str(win_size)], label='d:  '+str(dist)+' T/W: '+str(win_thre)+'/'+str(win_size))

    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")
    
    plt.legend(fontsize=12)
    plt.ylabel("True Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_sticker_true_prediction.png",bbox_inches='tight')
    plt.close() 

    plt.figure()

    for dist in dist_list:
        for win_thre,win_size in zip(win_thre,window_size):
            plt.plot(prob_list,false_prediction[dist][str(win_thre)+"/"+str(win_size)], label='d:  '+str(dist)+' T/W: '+str(win_thre)+'/'+str(win_size))

    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")

    plt.legend(fontsize=12)
    plt.ylabel("False Prediction Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_sticker_false_prediction.png",bbox_inches='tight')
    plt.close() 