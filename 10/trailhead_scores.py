def parse_map(input_file):
    """
    Parse the input file into a 2D grid of heights.
    """
    with open(input_file, 'r') as file:
        return [[int(c) for c in line.strip()] for line in file if line.strip()]


def is_within_bounds(x, y, grid):
    """
    Check if a position (x, y) is within the bounds of the grid.
    """
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def bfs_from_trailhead(x, y, grid):
    """
    Perform a BFS from a given trailhead (x, y) to count reachable '9's.
    """
    visited = set()  # Track visited positions
    queue = [(x, y, 0)]  # (current_x, current_y, current_height)
    reachable_nines = set()

    while queue:
        cx, cy, current_height = queue.pop(0)

        # If this position was already visited, skip it
        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))

        # If the current height is 9, count it
        if current_height == 9:
            reachable_nines.add((cx, cy))
            continue

        # Explore neighboring positions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy

            if is_within_bounds(nx, ny, grid) and (nx, ny) not in visited:
                # Ensure the next height is exactly one greater
                if grid[nx][ny] == current_height + 1:
                    queue.append((nx, ny, grid[nx][ny]))

    return len(reachable_nines)


def calculate_total_trailhead_scores(grid):
    """
    Calculate the total score for all trailheads in the grid.
    """
    total_score = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:  # Found a trailhead
                total_score += bfs_from_trailhead(x, y, grid)

    return total_score


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python hiking_trail_scores.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Parse the topographic map
        grid = parse_map(input_file)

        # Calculate total scores of all trailheads
        total_score = calculate_total_trailhead_scores(grid)

        print(f"The sum of the scores of all trailheads is: {total_score}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
