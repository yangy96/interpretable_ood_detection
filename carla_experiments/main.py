#
# Code written by : Souradeep Dutta,
#  duttaso@seas.upenn.edu, souradeep.dutta@colorado.edu
# Website : https://sites.google.com/site/duttasouradeep39/
#

import argparse
from memories import form_memories
import torch
import json





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_memories", type = bool, default = False, help = "Build memories switch" )
    parser.add_argument("--memory_source", default = "./training_carla")
    parser.add_argument("--memory_dir", default = "./memories/carla_memories_10_0.3/", help = "Destination for memories")
    parser.add_argument("--initial_memory_threshold", type = float, default = 0.3, help = "initial distance score")

    parser.add_argument("--predict_carla", type = bool, default = False, help = "Whether to predict carla ood")
    parser.add_argument("--test_carla_dir", default = "./out_night", help = "Destination for testing carla data")
    parser.add_argument("--detect_threshold", type = int, default = 20 , help = "detection threshold for detecting precipitation")
    parser.add_argument("--prob_threshold", type = float, default = 0.78 , help = "probability threshold of detection")
    parser.add_argument("--window_size", type = int, default = 5, help = "window size")
    parser.add_argument("--window_threshold", type = int, default = 5 , help = "window threshold")
    parser.add_argument("--task", default = "in" , help = "current task")
    
    args = parser.parse_args()
    #print(args)


    if args.build_memories :
        form_memories.build_memories_carla(args.memory_source, args.memory_dir, args.initial_memory_threshold)
    
    if args.predict_carla :
        stats = form_memories.run_carla_prediction(args.memory_dir, args.test_carla_dir, args.initial_memory_threshold, args.detect_threshold, args.prob_threshold, args.window_size,args.window_threshold, args.task)
        with open("./results/ood_result"+"_"+args.task+"_"+args.memory_dir.split("/")[-1]+"_"+str(args.window_size)+"_"+str(args.prob_threshold)+"_"+str(args.window_threshold)+".json", 'w') as outfile:
            json.dump(stats, outfile)
        outfile.close()
    
    #form_memories.dump_distances(args.memory_dir)

