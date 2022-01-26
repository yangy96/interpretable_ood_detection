import json
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_one_result(memory_dir,window_size,dist,window_threshold,task):
    prob_list = [0.8,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05]
    fp_prediction = []
    fn_prediction=[]
    if task == "heavy_rain":
        
        for prob in prob_list:
            in_file = "./ood_result"+"_in_"+task+"_"+str(dist)+"_"+str(window_size)+"_"+str(prob)+"_"+str(window_threshold)+".json"
            with open(os.path.join("results",in_file)) as json_file:
                data = json.load(json_file)
                fp_prediction.append(data["detection_rate"])
            json_file.close()
            out_file = "./ood_result"+"_out_"+task+"_"+str(dist)+"_"+str(window_size)+"_"+str(prob)+"_"+str(window_threshold)+".json"
            with open(os.path.join("results",out_file)) as json_file:
                data = json.load(json_file)
                fn_prediction.append(1-data["detection_rate"])
            json_file.close()
            
        plt.figure()

        plt.xticks(fontsize=18,weight="bold")
        plt.yticks(fontsize=18,weight="bold")
        plt.plot(prob_list,fp_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window_size))
        plt.legend(fontsize=12)
        plt.ylabel("False Positive Rate",fontsize=18,weight="bold")
        plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
        plt.savefig("./results/p_heavy_rain_false_positive_T_"+str(window_threshold)+"_W_"+str(window_size)+"_d_"+str(dist)+".png",bbox_inches='tight')
        plt.close() 

        plt.figure()
        plt.xticks(fontsize=18,weight="bold")
        plt.yticks(fontsize=18,weight="bold")
        plt.plot(prob_list,fn_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window_size))
        plt.legend(fontsize=12)
        plt.ylabel("False Negative Rate",fontsize=18,weight="bold")
        plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
        plt.savefig("./results/p_heavy_rain_false_negative_T_"+str(window_threshold)+"_W_"+str(window_size)+"_d_"+str(dist)+".png",bbox_inches='tight')
        plt.close() 

def plot_abalation():
    prob_list = [0.8,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05]
    fp_prediction = []
    fn_prediction=[]
    dist=0.2
    window_threshold = 5
    window_size = [5,10,15]
    task = "heavy_rain"
    for window in window_size:
        for prob in prob_list:
            in_file = "./ood_result"+"_in_"+task+"_"+str(dist)+"_"+str(window)+"_"+str(prob)+"_"+str(window_threshold)+".json"
            with open(os.path.join("results",in_file)) as json_file:
                data = json.load(json_file)
                fp_prediction.append(data["detection_rate"])
            json_file.close()
            out_file = "./ood_result"+"_out_"+task+"_"+str(dist)+"_"+str(window)+"_"+str(prob)+"_"+str(window_threshold)+".json"
            with open(os.path.join("results",out_file)) as json_file:
                data = json.load(json_file)
                fn_prediction.append(1-data["detection_rate"])
            json_file.close()
            
    plt.figure()
    for window in window_size:
        plt.plot(prob_list,fp_prediction, label='d:  '+str(dist)+' T/W: '+str(window_threshold)+'/'+str(window))

    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")

    plt.legend(fontsize=12)
    plt.ylabel("False Positive Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_heavy_rain_false_positive.png",bbox_inches='tight')
    plt.close() 

    plt.figure()
    for window in window_size:
        plt.plot(prob_list,fn_prediction, label='d:  '+str(dist)+' T/W: '+str(window)+'/'+str(window_size))
    plt.xticks(fontsize=18,weight="bold")
    plt.yticks(fontsize=18,weight="bold")

    plt.legend(fontsize=12)
    plt.ylabel("False Negative Rate",fontsize=18,weight="bold")
    plt.xlabel("Probability Density Threshold",fontsize=18,weight="bold")
    plt.savefig("./results/p_heavy_rain_false_negative.png",bbox_inches='tight')
    plt.close() 

                        
            
