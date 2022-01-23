# To reproduce OOD experiments detect change in carla simulation (section 6.1 & 6.2)


## Firstly

Create a result folder: 
`mkdir results`

## To run carla ood experiments

please run `python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2 --test_carla_dir ./oods_night --prob_threshold 0.92 --window_size 5 --window_threshold 5 --task oods_night`

## Section 6.1 Detect OOD-ness due to change in weather and lightning

### To reproduce the results in Table 1 (Heavy Rain Scenario)

run 
- `chmod 777 run_heavy_rain_experiments.sh`
- `./run_heavy_rain_experiments.sh`

It takes about ~40 minutes to finish the experiments <br>
When the script finishes (after viewing **finish both experiments**), it will print out all the experimental results and you can also find the results in *./results/carla_oods_night_exp_results.txt* and *./results/carla_oods_foggy_exp_results.txt*

### To reproduce the results in Table 2 (Night and Foggy Scenario)

run 
- `chmod 777 run_night_and_foggy.sh`
- `./run_night_and_foggy.sh`

It takes about ~5 minutes to finish the experiments <br>
When the script finishes (after viewing **finish both experiments**), it will print out all the experimental results and you can also find the results in *./results/carla_oods_night_exp_results.txt* and *./results/carla_oods_foggy_exp_results.txt*

### To reproduce Figure 11

We find that it takes about 5 hours to reproduce Figure 11 (3 plots total), so we provide a script to generate one plot only (~an hour). <br>

run 
- `chmod 777 run_heavy_rain_experiments_plot.sh`
- `./run_heavy_rain_experiments_plot.sh`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_false_positive_heavy_rain(11.a).png & ./results/p_false_negative_heavy_rain(11.b).png*


## Section 6.2 Detect OOD-ness due to change in front obstacles

### To reproduce the results in Table 3

run 
- `chmod 777 run_bike_experiments.sh`
- `./run_bike_experiments.sh`

It takes about ~3 minutes to finish the experiments <br>
When the script finishes (after viewing **"finish bike experiment 4/4"**), it will print out all the experimental results and you can also find the results in *./results/carla_ood_bikes_exp_results.txt*

## To generate memories

We already provide the memories we used in experiments (in *./memories/carla_memories_10_0.2* & *./memories/carla_memories_10_0.3* ), if want to generate the memories, <br>
run 
- `chmod 777 run_carla_memory_generation.sh`
- `./run_carla_memory_generation.sh`

but note this script overwrite the memories we provided and this new set of memory is not exactly the same as the original one. Please find the memories in *./memories/carla_memories_10_0.2* & *./memories/carla_memories_10_0.3* <br>
