#!/usr/bin/env python3

import sys
from collections import deque


def load_grid(input_file):
    """Read the grid from input and extract valid spaces, start, and end points."""
    spaces = set()
    start = end = None

    for row_idx, line in enumerate(map(str.rstrip, input_file)):
        for col_idx, char in enumerate(line):
            if char == '#':
                continue

            position = (row_idx, col_idx)
            spaces.add(position)

            if char == 'S':
                start = position
            elif char == 'E':
                end = position

    return spaces, start, end


def get_adjacent_positions(row, col):
    """Generate all valid neighbors for a given position."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        yield row + dr, col + dc


def compute_distances(grid, start):
    """Perform BFS to calculate distances from the start position."""
    queue = deque([start])
    distances = {start: 0}

    while queue:
        current = queue.popleft()

        for neighbor in get_adjacent_positions(*current):
            if neighbor in distances or neighbor not in grid:
                continue

            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances


def cheat_targets_within_range(row, col, max_range):
    """Generate possible cheat endpoints within the given range."""
    for distance in range(2, max_range + 1):
        for step in range(distance):
            remaining = distance - step
            yield (row + remaining, col + step), distance
            yield (row - remaining, col - step), distance
            yield (row + step, col - remaining), distance
            yield (row - step, col + remaining), distance


def find_valid_cheats(start_distances, end_distances, max_distance, max_cheat_length=2):
    """Identify and count valid cheats that shorten the path."""
    cheat_count = 0

    for position, start_distance in start_distances.items():
        for cheat_target, cheat_distance in cheat_targets_within_range(*position, max_cheat_length):
            if cheat_target not in end_distances:
                continue

            total_distance = start_distance + cheat_distance + end_distances[cheat_target]
            if total_distance <= max_distance:
                cheat_count += 1

    return cheat_count


def main():
    """Main function to execute the cheat evaluation."""
    if len(sys.argv) < 2:
        print("Usage: ./race_condition.py <input_file>")
        sys.exit(1)

    # Read and parse the input grid
    with open(sys.argv[1], 'r') as input_file:
        grid, start, end = load_grid(input_file)

    # Calculate distances from start and end points
    distances_from_start = compute_distances(grid, start)
    distances_from_end = compute_distances(grid, end)

    # Target distance after considering cheats
    max_allowed_distance = distances_from_start[end] - 100

    # Evaluate cheats for Part 1 (cheat length 2)
    part1_result = find_valid_cheats(distances_from_start, distances_from_end, max_allowed_distance, max_cheat_length=2)
    print(f"Result Part 1: {part1_result}")

    # Evaluate cheats for Part 2 (cheat length 20)
    part2_result = find_valid_cheats(distances_from_start, distances_from_end, max_allowed_distance, max_cheat_length=20)
    print(f"Result Part 2: {part2_result}")


if __name__ == "__main__":
    main()
