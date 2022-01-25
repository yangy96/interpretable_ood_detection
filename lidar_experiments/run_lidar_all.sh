echo "Warning: running this script takes about 12 hours"

for dist in 0.2 0.3
do
    for prob in 0.05 0.1 0.15 0.2 0.25 0.3
    do
        for window_threshold in 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 
        do 
            python3 main.py --predict_crash True --memory_source split_train_test/lidar_data/clean_data --memory_dir ./memories/LIDAR_memories_"$dist" --initial_memory_threshold $dist \
            --prob_threshold $prob --window_size 40 --window_threshold $window_threshold
        done
    done
done