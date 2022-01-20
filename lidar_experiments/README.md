# To reproduce OOD experiments for lidar data (section 7.3)

## To run lidar ood experiments

please run `python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --prob_threshold 0.05 --window_size 40 --window_threshold 15`

## To reproduce the results in Table 5

run `chmod 777 run_lidar_experiment.sh`<br>

run `./run_lidar_experiment.sh` <br>

When the script finishes (after viewing *"finish experiment 4/4"*), please find the results in *./results/lidar_exp_results.txt*

## To reproduce the Figure 10
We find that it takes about 14 hours to reproduce Figure 10 (12 plots total), so we provide a script to generate one plot. <br>
run `chmod 777 run_lidar_experiments_plot.sh` <br>
run `./run_lidar_experiments_plot.sh` <br>

Additionally, we provided dumped result for whole set of experiments and to generate figure 10, <br>
run `python3 main.py --plot_abalation_result True` <br>
//I leave this dumped results as future work 

## To produce memories
We already provide the memories we used in experiments, if want to reproduce the memories, but note this script may overwrite the memories we provided. <br>
run `chmod 777 run_lidar_memory_generation.sh` <br>
run `./run_lidar_memory_generation.sh`
