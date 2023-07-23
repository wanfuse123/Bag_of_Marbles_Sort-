#!/usr/bin/env python3

import numpy as np
import random
from time import time
from collections import Counter

# Define the sorting algorithms
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def radix_sort(arr):
    if len(arr) == 0:
        return []
    max_val = max(arr)
    digit_count = 1
    while max_val // digit_count > 0:
        buckets = [[] for _ in range(10)]
        for num in arr:
            digit = num // digit_count % 10
            buckets[digit].append(num)
        arr.clear()
        for bucket in buckets:
            arr.extend(bucket)
        digit_count *= 10
    return arr

def generate_random_subset_indices(dataset_size, subset_size):
    return random.sample(range(dataset_size), subset_size)

def recreate_original_set_from_buckets(buckets, dataset_size):
    recreated_dataset = []
    for value, count in buckets.items():
        recreated_count = round(count / len(buckets) * dataset_size)
        recreated_dataset.extend([value] * recreated_count)
    return recreated_dataset

def save_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(f"{item}\n")

# Generate random dataset
dataset_size = 3000000

# Generate normally distributed dataset
mean = 5000  # mean
std_dev = 1000  # standard deviation
dataset_size = 3000000
dataset = list(np.random.normal(mean, std_dev, dataset_size).astype(int))

#dataset = [random.randint(0, 100000) for _ in range(dataset_size)]
np.random.shuffle(dataset)

# Define the sorting algorithms
algorithms = [radix_sort]

# Define the subset sizes to test
subset_sizes = [2000000, 200000, 100000, 25000]

# Prepare to store the summaries
summaries = []

# Perform the sampling
for subset_size in subset_sizes:
    for sorting_algorithm in algorithms:
        print(f"Sorting Algorithm: {sorting_algorithm.__name__}")
        print("-------------------------")
        print(f"Subset Size: {subset_size}")

        # Draw the subset indices in random order, and build buckets at the same time
        subset_indices = generate_random_subset_indices(dataset_size, subset_size)
        buckets = Counter()
        subset = []
        for i in subset_indices:
            subset.append(dataset[i])
            buckets[dataset[i]] += 1

        # Save original subset to file
        save_list_to_file(subset, f"original_subset_{sorting_algorithm.__name__}_{subset_size}.txt")

        # Sort the subset
        start_time = time()
        sorted_subset = sorting_algorithm(subset)
        subset_sort_time = time() - start_time

        # Save sorted subset to file
        save_list_to_file(sorted_subset, f"sorted_subset_{sorting_algorithm.__name__}_{subset_size}.txt")

        # Recreate the original dataset from the buckets
        recreated_dataset = recreate_original_set_from_buckets(buckets, dataset_size)

        # Sort the recreated dataset
        start_time = time()
        sorted_recreated_dataset = sorting_algorithm(recreated_dataset)
        full_set_sort_time = time() - start_time

        # Save recreated dataset to file
        save_list_to_file(sorted_recreated_dataset, f"recreated_dataset_{sorting_algorithm.__name__}_{subset_size}.txt")

        # Verify the recreation against the original dataset
        match_count = sum((Counter(sorted_recreated_dataset) & Counter(dataset)).values())

        # Save the summary for this run
        summaries.append({
            'Sorting Algorithm': sorting_algorithm.__name__,
            'Subset Size': subset_size,
            'Full Set Size': dataset_size,
            'Number of Unique Elements': len(buckets),
            'Subset Sort Time': subset_sort_time,
            'Full Set Sort Time': full_set_sort_time,
            'Recreated Match Count': match_count
        })

        print(f"  Full Set Size: {dataset_size}")
        print(f"  Subset Size: {subset_size}")
        print(f"  Number of Unique Elements: {len(buckets)}")
        print(f"  Subset Sort Time: {subset_sort_time}")
        print(f"  Full Set Sort Time: {full_set_sort_time}")
        print(f"  Recreated Match Count: {match_count}")
        print()

# Print the summaries
print("=" * 80)
print("Summary of Results")
print("-----------------")

for summary in summaries:
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print()
