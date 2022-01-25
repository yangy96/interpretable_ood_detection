# To reproduce OOD experiments for lidar data (section 7.3)

## To reproduce the results in Table 5

- for generating results for 1 row of the table, ex. W (window_size) = 40, tau (window_threshold) = 15, alpha (prob_threshold) = 0.05, d (initial_memory_threshold) = 0.3 and LIDAR_memories_$d$ = LIDAR_memories_0.3: 
`python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --prob_threshold 0.05 --window_size 40 --window_threshold 15 --initial_memory_threshold 0.3`
- for generating results for the entire table (4 rows), please run the following two commands:
- `chmod 777 run_lidar_experiments.sh`
- `./run_lidar_experiments.sh`

It takes about 20 minutes for generating results of the entire Table 5, i.e. running the script run_lidar_experiments.sh <br>
When the script finishes (i.e. after printing **"finish experiment 4/4"**), you will see all the experimental results printed on console. You can also find the results in *./results/lidar_exp_results.txt*

## To reproduce Figure 10
We find that it takes about 14 hours to reproduce Figure 10 (12 plots total and 18 points in each plot), so we provide a script to generate one plot. <br>

- for generating one plot for viewing influence of different window threshold with selected parameters, ex. alpha = 0.05, d = 0.3, run following commands
- `chmod 777 run_lidar_experiments_plot.sh`
- `./run_lidar_experiments_plot.sh 0.05 0.3`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_lidar_true_prediction_alpha_$alpha$_d_$d$.png & ./results/p_lidar_false_prediction_alpha_$alpha$_d_$d$.png*


## To generate memories from scratch (Optional)

The above experiments use the memories that were used in the experiments for the paper (in *./memories/LIDAR_memories_0.2* & *LIDAR_memories_0.3*). If you want to generate the memories from scratch and then run the aboove experiments, then please run the following commands before running the experiments for Table 5 and Figure 10 <br>

- `chmod 777 run_lidar_memory_generation.sh`
- `./run_lidar_memory_generation.sh`

Note: The generated memories might differ from the exisitng ones, depending on the random seed. 
