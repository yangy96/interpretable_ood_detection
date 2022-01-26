rm -f ./results/carla_sticker_exp_results.txt

python3 main.py --predict_carla True --initial_memory_threshold 0.5 --memory_dir ./memories/carla_adv_memories_10_0.5 --test_carla_dir ./test_attacks \
        --prob_threshold 0.05 --window_size 5 --window_threshold 5

echo "finish sticker experiments 1/4"

python3 main.py --predict_carla True --initial_memory_threshold 0.5 --memory_dir ./memories/carla_adv_memories_10_0.5 --test_carla_dir ./test_attacks \
        --prob_threshold 0.1 --window_size 5 --window_threshold 5

echo "finish sticker experiments 2/4"

python3 main.py --predict_carla True --initial_memory_threshold 0.6 --memory_dir ./memories/carla_adv_memories_10_0.6 --test_carla_dir ./test_attacks \
        --prob_threshold 0.2 --window_size 5 --window_threshold 5

echo "finish sticker experiments 3/4"

python3 main.py --predict_carla True --initial_memory_threshold 0.6 --memory_dir ./memories/carla_adv_memories_10_0.6 --test_carla_dir ./test_attacks \
        --prob_threshold 0.25 --window_size 5 --window_threshold 5

echo "finish sticker experiments 4/4"