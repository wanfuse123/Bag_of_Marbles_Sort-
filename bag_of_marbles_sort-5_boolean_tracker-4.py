#!/usr/bin/env python3

from collections import Counter
import numpy as np
import time
import random

def generate_checksum(arr):
    checksum = sum(arr) % 1000000007
    length = len(str(checksum))
    return checksum, length

def calculate_accuracy(original_dataset, recreated_dataset):
    original_mean = np.mean(original_dataset)
    original_std = np.std(original_dataset)
    recreated_mean = np.mean(recreated_dataset)
    recreated_std = np.std(recreated_dataset)

    mean_diff = abs(original_mean - recreated_mean)
    std_diff = abs(original_std - recreated_std)

    return mean_diff, std_diff

def calculate_differences(sorted_original_dataset, sorted_recreated_dataset):
    same_values = 0
    same_position = 0
    duplicated_values = 0
    different_values = 0
    left_out_values = len(sorted_original_dataset) - len(sorted_recreated_dataset)

    recreated_values_counter = Counter(sorted_recreated_dataset)

    for idx, value in enumerate(sorted_original_dataset[:len(sorted_recreated_dataset)]):
        if value in recreated_values_counter:
            same_values += 1
            if value == sorted_recreated_dataset[idx]:
                same_position += 1
            if recreated_values_counter[value] > 1:
                # Increment only once for each value that appears more than once
                duplicated_values += 1
            recreated_values_counter[value] -= 1  # Decrement the counter for the value
        else:
            different_values += 1

    return same_values, same_position, duplicated_values, different_values, left_out_values

def recreate_original_distribution_from_subset(subset, original_size, original_mean, original_std):
    start_time_stats = time.time()
    subset_mean = np.mean(subset)
    subset_std = np.std(subset)
    stats_time = time.time() - start_time_stats

    start_time_recreation = time.time()
    scaling_factor_mean = original_mean / subset_mean
    scaling_factor_std = original_std / subset_std
    recreated = np.random.normal(original_mean, original_std, original_size)
    recreate_time = time.time() - start_time_recreation

    return recreated.astype(int), stats_time, recreate_time

# Generate random dataset
dataset_size = 30000000
mean = 5000  # mean
std_dev = 1000  # standard deviation
original_dataset = list(np.random.normal(mean, std_dev, dataset_size).astype(int))

start_time_original = time.time()
sorted_original_dataset = sorted(original_dataset[:])
checksum_original, checksum_length_original = generate_checksum(sorted_original_dataset) # Fix here
time_to_process_original = time.time() - start_time_original
# Define the subset sizes to test
subset_sizes = [2000000, 200000, 100000, 25000]

# Perform the sampling
for subset_size in subset_sizes:
    np.random.shuffle(original_dataset)
    subset = original_dataset[:subset_size]

    print(f"Subset Size: {subset_size}")
    print("-------------------------")

    start_time = time.time()
    recreated_dataset, stats_time, recreate_time = recreate_original_distribution_from_subset(subset, dataset_size, mean, std_dev)
    sorted_recreated_dataset = sorted(recreated_dataset)  # Add this line to sort the recreated dataset
    total_time = time.time() - start_time


    checksum_recreated, checksum_length_recreated = generate_checksum(recreated_dataset)

    print(f"  Length of Original Dataset: {dataset_size}")
    print(f"  Checksum of Original Dataset: {checksum_original} (length {checksum_length_original})")
    print(f"  Time to process original dataset: {time_to_process_original:.6f} seconds")
    print(f"  Length of Recreated Dataset: {len(recreated_dataset)}")
    print(f"  Checksum of Recreated Dataset: {checksum_recreated} (length {checksum_length_recreated})")
    print(f"  Time to calculate statistics: {stats_time:.6f} seconds")
    print(f"  Time to recreate dataset: {recreate_time:.6f} seconds")
    print(f"  Total time for subset: {total_time:.6f} seconds")
    print()

    
    same_values, same_position, duplicated_values, different_values, left_out_values = calculate_differences(
        sorted_original_dataset, sorted_recreated_dataset)

    print(f"  Same values: {same_values}")
    print(f"  Same position: {same_position}")
    print(f"  Duplicated values: {duplicated_values}")
    print(f"  Different values: {different_values}")
    print(f"  Left out values: {left_out_values}")
    print()
    
mean_diff, std_diff = calculate_accuracy(original_dataset, recreated_dataset)
print(f"  Difference in mean: {mean_diff}")
print(f"  Difference in standard deviation: {std_diff}")

print("Done!")
