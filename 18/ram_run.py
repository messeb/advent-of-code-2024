import sys
from collections import deque

def parse_input(filename):
    """Parse input file to extract byte positions."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    byte_positions = [tuple(map(int, line.split(','))) for line in lines]
    return byte_positions

def simulate_corruption(grid_size, byte_positions, num_bytes):
    """Simulate falling bytes and mark the grid as corrupted."""
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in byte_positions[:num_bytes]:
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python ram_run.py <input_file>")
        sys.exit(1)

    # Parse input file
    filename = sys.argv[1]
    byte_positions = parse_input(filename)

    # Constants
    GRID_SIZE = 71  # From 0 to 70
    NUM_BYTES = 1024  # First kilobyte

    # Simulate corruption
    grid = simulate_corruption(GRID_SIZE, byte_positions, NUM_BYTES)

    # Find shortest path
    shortest_path = bfs_shortest_path(grid)

    if shortest_path != -1:
        print(f"The minimum number of steps to reach the exit is: {shortest_path}")
    else:
        print("There is no valid path to the exit.")

if __name__ == "__main__":
    main()
