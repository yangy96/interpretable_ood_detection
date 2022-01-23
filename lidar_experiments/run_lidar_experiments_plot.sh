echo "Warning: running this script takes about an hour"

prob=$1
dist=$2

echo "probability threshold: $1, distance: $2"

for window_threshold in 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 
do 
    python3 main.py --predict_crash True --memory_source split_train_test/lidar_data/clean_data --memory_dir ./memories/LIDAR_memories_"$dist" --initial_memory_threshold $dist \
    --prob_threshold $prob --window_size 40 --window_threshold $window_threshold
done

python3 main.py --plot_one_result True --memory_dir ./memories/LIDAR_memories_"$dist" --initial_memory_threshold $dist \
--prob_threshold $prob --window_size 40

echo "finish one graph in the figure"