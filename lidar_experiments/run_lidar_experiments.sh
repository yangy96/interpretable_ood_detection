rm -f ./results/lidar_exp_results.txt

python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --initial_memory_threshold 0.3 \
--prob_threshold 0.05 --window_size 40 --window_threshold 15

echo "finish experiment 1/4"

python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.3 --initial_memory_threshold 0.3 \
--prob_threshold 0.1 --window_size 40 --window_threshold 17

echo "finish experiment 2/4"

python3 main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.2 --initial_memory_threshold 0.2 \
--prob_threshold 0.05 --window_size 40 --window_threshold 11

echo "finish experiment 3/4"

python3 -u main.py --predict_crash True --memory_dir ./memories/LIDAR_memories_0.2 --initial_memory_threshold 0.2 \
--prob_threshold 0.1 --window_size 40 --window_threshold 15

echo "finish experiment 4/4"