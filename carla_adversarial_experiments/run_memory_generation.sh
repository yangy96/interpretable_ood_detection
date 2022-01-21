#!/bin/bash

python3 main.py --build_memories True --memory_source ./training --memory_dir ./memories/carla_adv_memories_10_0.5 --initial_memory_threshold 0.5

echo "finish memory generation with initial distance threshold 0.5"

python3 main.py --build_memories True --memory_source ./training --memory_dir ./memories/carla_adv_memories_10_0.6 --initial_memory_threshold 0.6

echo "finish memory generation with initial distance threshold 0.6"

echo "memory generation done"