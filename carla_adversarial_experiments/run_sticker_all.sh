echo "Warning: running this script takes about 12 hour"

for dist in 0.5 0.6
do
    for win_thre in 5 7 9
    do
        for prob in 0.05 0.1 0.2 0.25 0.3 0.35 0.4 0.45 0.5
        do 
            python3 main.py --predict_carla True --initial_memory_threshold $dist --memory_dir ./memories/carla_adv_memories_10_"$dist" --test_carla_dir ./test_attacks \
                --prob_threshold $prob --window_size 10 --window_threshold $win_thre
        done
    done
done

for dist in 0.5 0.6
do
    for prob in 0.05 0.1 0.2 0.25 0.3 0.35 0.4 0.45 0.5
    do 
        python3 main.py --predict_carla True --initial_memory_threshold $dist --memory_dir ./memories/carla_adv_memories_10_"$dist" --test_carla_dir ./test_attacks \
            --prob_threshold $prob --window_size 5 --window_threshold 5
    done
done
