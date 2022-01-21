echo "Warning: running this script takes about 1.5 hour"

for prob in 0.05 0.1 0.2 0.25 0.3 0.35 0.4 0.45 0.5
do 
    python3 main.py --predict_carla True --initial_memory_threshold 0.6 --memory_dir ./memories/carla_adv_memories_10_0.6 --test_carla_dir ./test_attacks \
        --prob_threshold $prob --window_size 5 --window_threshold 5
done

python3 main.py --plot_one_result True --memory_dir ./memories/carla_adv_memories_10_0.6 --initial_memory_threshold 0.6 --window_size 5 --window_threshold 5

echo "finish one graph in the figure"
