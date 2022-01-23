echo "Warning: running this script takes about 1.5 hour"

win_thre=$1
win_size=$2
dist=$3

echo "window threshold: $1, window size: $2, distance: $3"

for prob in 0.05 0.1 0.2 0.25 0.3 0.35 0.4 0.45 0.5
do 
    python3 main.py --predict_carla True --initial_memory_threshold $dist --memory_dir ./memories/carla_adv_memories_10_"$dist" --test_carla_dir ./test_attacks \
        --prob_threshold $prob --window_size $win_size --window_threshold $win_thre
done

python3 main.py --plot_one_result True --memory_dir ./memories/carla_adv_memories_10_"$dist" --initial_memory_threshold $dist --window_size $win_size --window_threshold $win_thre

echo "finish one graph in the figure"
