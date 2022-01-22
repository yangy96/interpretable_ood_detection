# To reproduce OOD experiments for lidar data (section 7.3)

## Firstly

Create a result folder: 
`mkdir results`

## To reproduce the results in Table 5

- for generating results for 1 row of the table, ex. W (window_size) = 40, tau (window_threshold) = 15, alpha (prob_threshold) = 0.05, d (initial_memory_threshold) = 0.3 and LIDAR_memories_$d$ = LIDAR_memories_0.3: 
`python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --prob_threshold 0.05 --window_size 40 --window_threshold 15 --initial_memory_threshold 0.3`
- for generating results for the entire table (4 rows), please run the following two commands:
- `chmod 777 run_lidar_experiments.sh`
- `./run_lidar_experiments.sh`

It takes about 20 minutes for generating results of the entire Table 5, i.e. running the script run_lidar_experiments.sh <br>
When the script finishes (i.e. after printing **"finish experiment 4/4"**), you will see all the experimental results printed on console. You can also find the results in *./results/lidar_exp_results.txt*

## To reproduce Figure 10
We find that it takes about 14 hours to reproduce Figure 10 (12 plots total and ? points in each plot), so we provide a script to generate one plot. <br>
run 
- `chmod 777 run_lidar_experiments_plot.sh`
- `./run_lidar_experiments_plot.sh`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_correct_prediction_lidar_(10.a).png & ./results/results/p_false_prediction_lidar_(10.b).png*

Additionally, we provided dumped result for whole set of experiments and to generate figure 10, <br>
run 
- `python3 main.py --plot_abalation_result True` <br>
Note: I am currently running dumped results <br>

When the script finishes (after viewing **"finish dump images**), please find the plots in *./results/lidar_exp_results.txt*

## To generate memories from scratch (Optinal)

The above experiments use the memories that we provided as used in the experiments for the paper (in *./memories/LIDAR_memories_0.2* & *LIDAR_memories_0.3*), if want to generate the memories and then run the above experiments, then please run the following commands before running the experiments for Table 5 and Figure 10 <br>

- `chmod 777 run_lidar_memory_generation.sh`
- `./run_lidar_memory_generation.sh`

but note this script overwrite the memories we provided and this new set of memory is not exactly the same as the original one. Please find the memories in *./memories/LIDAR_memories_0.2* & *./memories/LIDAR_memories_0.3* <br>
