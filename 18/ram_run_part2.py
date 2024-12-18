import sys
from collections import deque

def parse_input(filename):
    """Parse input file to extract byte positions."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    byte_positions = [tuple(map(int, line.split(','))) for line in lines]
    return byte_positions

def simulate_corruption(grid_size, byte_positions, corrupted_count):
    """Simulate falling bytes and mark the grid as corrupted."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in byte_positions[:corrupted_count]:
        grid[y][x] = '#'
    return grid

def bfs_shortest_path(grid):
    """Find the shortest path using Breadth-First Search."""
    n = len(grid)
    start = (0, 0)
    end = (n - 1, n - 1)
    if grid[start[1]][start[0]] == '#' or grid[end[1]][end[0]] == '#':
        return -1  # No path if start or end is corrupted

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    queue = deque([(start, 0)])  # (position, steps)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[ny][nx] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    
    return -1  # No path found

def find_first_blocking_byte(grid_size, byte_positions):
    """Find the first byte that blocks the path to the exit."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    for idx, (x, y) in enumerate(byte_positions):
        grid[y][x] = '#'
        if bfs_shortest_path(grid) == -1:
            return x, y

    return None  # Path never gets fully blocked

def main():
    if len(sys.argv) != 2:
        print("Usage: python ram_run_part2.py <input_file>")
        sys.exit(1)

    # Parse input file
    filename = sys.argv[1]
    byte_positions = parse_input(filename)

    # Constants
    GRID_SIZE = 71  # From 0 to 70

    # Part Two: Find the first blocking byte
    first_blocking_byte = find_first_blocking_byte(GRID_SIZE, byte_positions)
    if first_blocking_byte:
        print(f"{first_blocking_byte[0]},{first_blocking_byte[1]}")
    else:
        print("No byte completely blocks the path.")

if __name__ == "__main__":
    main()
