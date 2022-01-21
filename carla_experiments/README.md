# To reproduce OOD experiments detect change in carla simulation (section 6.1 & 6.2)

## To run carla ood experiments

please run `python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2 --test_carla_dir ./oods_night --prob_threshold 0.92 --window_size 5 --window_threshold 5 --task oods_night`

## Section 6.1 Detect OOD-ness due to change in weather and lightning

### To reproduce the results in Table 1 (Heavy Rain Scenario)

### To reproduce the results in Table 2 (Night and Foggy Scenario)

run 
- `chmod 777 run_night_and_foggy.sh`
- `./run_night_and_foggy.sh`

It takes about ~5 minutes to finish the experiments <br>
When the script finishes (after viewing **finish both experiments**), it will print out all the experimental results and you can also find the results in *./results/carla_oods_night_exp_results.txt* and *./results/carla_oods_foggy_exp_results.txt*

### To reproduce Figure 11



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
