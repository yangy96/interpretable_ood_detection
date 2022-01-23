# To reproduce OOD experiments detect change in carla simulation (section 6.1 & 6.2)

## Section 6.1 Detect OOD-ness due to change in weather and lightning

### To reproduce the results in Table 1 (Heavy Rain Scenario)

- for generating results for 1 row of the table, ex. W (window_size) = 5, tau (window_threshold) = 5, alpha (prob_threshold) = 0.92, d (initial_memory_threshold) = 0.2 and memory_dir =  ./memories/carla_memories_10_$d$ = ./memories/carla_memories_10_0.2, task = heavy_rain (automatically run both in-dist exp & ood exp): `python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2  --initial_memory_threshold 0.2 --test_carla_dir ./test_carla --prob_threshold 0.92 --window_size 5 --window_threshold 5 --task heavy_rain`

- for generating results for the entire table (4 rows), please run the following two commands:
- `chmod 777 run_heavy_rain_experiments.sh`
- `./run_heavy_rain_experiments.sh`

It takes about ~40 minutes to finish the experiments <br>
When the script finishes (after viewing **finish both experiments**), it will print out all the experimental results and you can also find the results in *./results/carla_oods_night_exp_results.txt* and *./results/carla_oods_foggy_exp_results.txt*

### To reproduce the results in Table 2 (Night and Foggy Scenario)

- for generating results for 1 row of the table, ex. W (window_size) = 5, tau (window_threshold) = 5, alpha (prob_threshold) = 0.92, d (initial_memory_threshold) = 0.2 and memory_dir =  ./memories/carla_memories_10_$d$ = ./memories/carla_memories_10_0.2, task = oods_night (task choices are: oods_night, oods_foggy in this experiment) test_carla_dir=./test_carla/$task: `python3 main.py --predict_carla True --memory_dir ./memories carla_memories_10_0.2  --initial_memory_threshold 0.2 --test_carla_dir ./test_carla/oods_night --prob_threshold 0.92 --window_size 5 --window_threshold 5 --task oods_night`

- for generating results for the entire table (8 rows), please run the following two commands:
- `chmod 777 run_night_and_foggy.sh`
- `./run_night_and_foggy.sh`

It takes about ~5 minutes to finish the experiments <br>
When the script finishes (after viewing **finish both experiments**), it will print out all the experimental results and you can also find the results in *./results/carla_oods_night_exp_results.txt* and *./results/carla_oods_foggy_exp_results.txt*

### To reproduce Figure 11

We find that it takes about 5 hours to reproduce Figure 11 (3 plots total and 21 points in each plot), so we provide a script to generate one plot only (~an hour). <br>
- for generating one plot for viewing influence of different window threshold with selected parameters, ex. tau (window_threshold) = 5, W (window_size) = 10, run following commands
run 
- `chmod 777 run_heavy_rain_experiments_plot.sh`
- `./run_heavy_rain_experiments_plot.sh 5 10`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_heavy_rain_false_positive_tau_$window_threshold_T_$window_size_d_$dist.png"* & *./results/p_heavy_rain_false_negative_tau_$window_threshold_T_$window_size_d_$dist.png*


## Section 6.2 Detect OOD-ness due to change in front obstacles

### To reproduce the results in Table 3

- for generating results for 1 row of the table, ex. W (window_size) = 5, tau (window_threshold) = 5, alpha (prob_threshold) = 0.92, d (initial_memory_threshold) = 0.2 and memory_dir =  ./memories/carla_memories_10_$d$ = ./memories/carla_memories_10_0.2, task = oods_bike: `python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2  --test_carla_dir ./test_carla/oods_bike --prob_threshold 0.92 --window_size 5 --window_threshold 5 --task oods_bike`

- for generating results for the entire table (4 rows), please run the following two commands:
- `chmod 777 run_bike_experiments.sh`
- `./run_bike_experiments.sh`

It takes about ~3 minutes to finish the experiments <br>
When the script finishes (after viewing **"finish bike experiment 4/4"**), it will print out all the experimental results and you can also find the results in *./results/carla_ood_bikes_exp_results.txt*

## To generate memories from scratch (Optional)

We already provide the memories we used in experiments (in *./memories/carla_memories_10_0.2* & *./memories/carla_memories_10_0.3* ), if want to generate the memories, <br>
run 
- `chmod 777 run_carla_memory_generation.sh`
- `./run_carla_memory_generation.sh`

Note: The generated memories might differ from the exisitng ones, depending on the random seed. 
