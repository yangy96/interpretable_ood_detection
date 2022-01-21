# To reproduce OOD experiments for lidar data (section 7.3)

## To run lidar ood experiments

please run `python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --prob_threshold 0.05 --window_size 40 --window_threshold 15`

## To reproduce the results in Table 5

run 
- `chmod 777 run_lidar_experiment.sh`
- `./run_lidar_experiment.sh`

It takes about 20 minutes to finish the experiments <br>
When the script finishes (after viewing **"finish experiment 4/4"**), it will print out all the experimental results and you can also find the results in *./results/lidar_exp_results.txt*

## To reproduce the Figure 10
We find that it takes about 14 hours to reproduce Figure 10 (12 plots total), so we provide a script to generate one plot. <br>
run 
- `chmod 777 run_lidar_experiments_plot.sh`
- `./run_lidar_experiments_plot.sh`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_correct_prediction_lidar_(10.a).png & ./results/results/p_false_prediction_lidar_(10.b).png*

Additionally, we provided dumped result for whole set of experiments and to generate figure 10, <br>
run 
- `python3 main.py --plot_abalation_result True` <br>
Note: I am currently running dumped results <br>

When the script finishes (after viewing **"finish dump images**), please find the plots in *./results/lidar_exp_results.txt*

## To produce memories

We already provide the memories we used in experiments, if want to reproduce the memories, <br>
run 
- `chmod 777 run_lidar_memory_generation.sh`
- `./run_lidar_memory_generation.sh`

but note this script overwrite the memories we provided and this new set of memory is not exactly the same as the original one. <br>
