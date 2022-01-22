echo "Warning: running this script takes about 1.5 hour"

for prob in 0.8 0.85 0.86 0.87 0.88 0.89 0.9 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99 1.0 1.01 1.02 1.03 1.04 1.05
do 
    python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2  --initial_memory_threshold 0.2 --test_carla_dir ./test_carla/in_test \
    --prob_threshold $prob --window_size 5 --window_threshold 5 --task heavy_rain

    python3 main.py --predict_carla True --memory_dir ./memories/carla_memories_10_0.2  --initial_memory_threshold 0.2 --test_carla_dir ./test_carla/oods_heavy_rain \
    --prob_threshold $prob --window_size 5 --window_threshold 5 --task heavy_rain
done

python3 main.py --plot_one_result True --memory_dir ./memories/carla_memories_10_0.2 --initial_memory_threshold 0.2 --window_size 5 --window_threshold 5 --task heavy_rain

echo "finish one graph in the figure"