# To run OOD experiments to detect perturbations by adversarial attack (section 6.3)

## To run OOD detecion on adversarial sticker experiments

please run `python3 main.py --predict_carla True --initial_memory_threshold 0.5 --memory_dir ./memories/carla_adv_memories_10_0.5 --test_carla_dir ./test_attacks --prob_threshold 0.05 --window_size 5 --window_threshold 5`

## To reproduce the results in Table 4

run 
- `chmod 777 run_sticker_experiments.sh`
- `./run_sticker_experiments.sh`

It takes about 30 minutes to finish the experiments <br>
When the script finishes (after viewing **"finish experiment 4/4"**), it will print out all the experimental results and you can also find the results in *./results/carla_sticker_exp_results.txt*

## To reproduce Figure 6
We find that it takes about 10 hours to reproduce Figure 6 (8 plots total), so we provide a script to generate one plot only (~an hour). <br>

run 
- `chmod 777 run_sticker_experiments_plot.sh`
- `./run_sticker_experiments_plot.sh`

When the script finishes (after viewing **"finish one graph in the figure"**), please find the plots in *./results/p_correct_prediction_carla_sticker(6.a).png & ./results/p_false_prediction_carla_sticker(6.b).png*

Additionally, we provided dumped result for whole set of experiments and to generate figure 6, <br>
run 
- `python3 main.py --plot_abalation_result True` <br>
Note: I am currently running dumped results <br>

When the script finishes (after viewing **"finish dump images**), please find the plots in *./saved_results/p_correct_prediction_carla_sticker(6.a).png* & *./saved_results/p_correct_prediction_carla_sticker(6.b).png*

## To generate memories

We already provide the memories we used in experiments (in *./memories/carla_adv_memories_10_0.5* & *./memories/carla_adv_memories_10_0.6* ), if want to generate the memories, <br>
run 
- `chmod 777 run_memory_generation.sh`
- `./run_memory_generation.sh`

but note this script overwrite the memories we provided and this new set of memory is not exactly the same as the original one. Please find the memories in *./memories/carla_adv_memories_10_0.5* & *./memories/carla_adv_memories_10_0.6* <br>
