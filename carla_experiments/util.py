import json
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--read_file", default = "")

args = parser.parse_args()
print(args)

window_size=[5,10]
name = args.read_file.split("_")
total_number = {"in":27}

delay_list=[]
false_positive=[]
false_negative=[]

index=[]
prob_list={"0.2":[0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95],"0.25":[0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95], "0.3":[0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8],"0.35":[0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8]}
prob_list={"0.2":[0.92],"0.3":[0.78]}
file_list = ["bike_oods","out_foggy","out_night"]
threshold_list={"bike_oods":20,"out_foggy":0,"out_night":10}

for file in file_list:
    for dist in["0.2","0.3"]:
        detection_rate=[]
        average_delay=[]
        index=[]
        for prob in prob_list[dist]:
            index.append(prob)
            for i in window_size:
                in_file = "memory_generation_"+file+"_"+dist+"_"+str(i)+"_"+str(prob)+".json"
                with open(os.path.join("",in_file)) as json_file:
                    data = json.load(json_file)
                    for p in data.keys():
                        index.append(str(p)+"/"+str(i))
                        #index = str(p)+"/"+str(i)
                        
                        print("detection rate ",data[p]["detection_rate"])
                        detection_rate.append(data[p]["detection_rate"])
                        print("detection frame list ",data[p]["detect_frame_list"])
                        new_frame=[]
                        for m in data[p]["detect_frame_list"]:
                            if m > threshold_list[file]:
                                new_frame.append(m-threshold_list[file])
                            else:
                                new_frame.append(0)
                        print(file,new_frame)
                        if(len(data[p]["detect_frame_list"])>0):
                            print("average window delay ",sum(new_frame)/len(new_frame))
                            average_delay.append(sum(new_frame)/len(new_frame))
                        else:
                            print("average window delay ")
                            average_delay.append(None)
                    json_file.close()
            average_delay.append('')
            detection_rate.append('')
                    #index.append('')
                    
            
                
        print(len(detection_rate),len(average_delay),index)

        store_data={"detection rate ":detection_rate,"average delay":average_delay}
        df = pd.DataFrame(store_data, index=pd.Index(index))
        print(df)
        df.to_excel('carla_'+file+'_'+dist+'.xlsx')
