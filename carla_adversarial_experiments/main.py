#
# Code written by : Souradeep Dutta,
#  duttaso@seas.upenn.edu, souradeep.dutta@colorado.edu
# Website : https://sites.google.com/site/duttasouradeep39/
#

import argparse
from memories import form_memories
import torch
import json
from util import plot_one_result,plot_abalation
import os
import warnings
warnings.filterwarnings("ignore")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_memories", type = bool, default = False, help = "Build memories switch" )
    parser.add_argument("--memory_source", default = "./training")
    parser.add_argument("--memory_dir", default = "./memories/carla_adv_memories_10_0.6/", help = "Destination for memories")
    parser.add_argument("--initial_memory_threshold", type = float, default = 0.6, help = "initial distance score")

    parser.add_argument("--predict_carla", type = bool, default = False, help = "Whether to predict carla ood")
    parser.add_argument("--test_carla_dir", default = "images_attacks", help = "Destination for testing carla data")
    parser.add_argument("--prob_threshold", type = float, default = 0.1 , help = "probability threshold of detection")
    parser.add_argument("--window_size", type = int, default = 5 , help = "window size")
    parser.add_argument("--window_threshold", type = int, default = 5 , help = "window threshold")
    parser.add_argument("--plot_one_result", type = bool, default = False , help = "plot for one graph only")
    parser.add_argument("--plot_full_abalation", type = bool, default = False , help = "plot for full abalation")

    args = parser.parse_args()


    if args.build_memories :
        form_memories.build_memories_carla(args.memory_source, args.memory_dir, args.initial_memory_threshold)
    
    if args.predict_carla :
        if not os.path.exists('./results'):
            os.mkdir('./results')
        stats = form_memories.run_carla_prediction(args.memory_dir, args.test_carla_dir, args.initial_memory_threshold, args.prob_threshold, args.window_size, args.window_threshold)
        with open("./results/ood_result_adv"+"_"+str(args.initial_memory_threshold)+"_"+str(args.window_size)+"_"+str(args.prob_threshold)+"_"+str(args.window_threshold)+".json", 'w') as outfile:
            json.dump(stats, outfile)
        outfile.close()

    if args.plot_one_result :
        plot_one_result(args.memory_dir,args.window_size,args.initial_memory_threshold,args.window_threshold)

    if args.plot_full_abalation:
        plot_abalation()