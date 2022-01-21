#!/bin/bash


python3 main.py --build_memories True --memory_source ./training_data --memory_dir ./memories/carla_memories_10_0.2 --initial_memory_threshold 0.2

echo "memory generation with initial distance threshold 0.2"

python3 main.py --build_memories True --memory_source ./training_data --memory_dir ./memories/carla_memories_10_0.3 --initial_memory_threshold 0.3

echo "memory generation with initial distance threshold 0.3"

echo "memory generation done"