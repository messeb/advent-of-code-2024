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


def dfs_count_paths(x, y, grid, current_height, visited):
    """
    Perform a DFS to count all distinct paths from (x, y) to any 9.
    """
    if not is_within_bounds(x, y, grid) or (x, y) in visited or grid[x][y] != current_height:
        return 0

    # If we reach a height of 9, this is a valid path
    if current_height == 9:
        return 1

    visited.add((x, y))  # Mark current position as visited

    # Explore all cardinal directions
    path_count = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if is_within_bounds(nx, ny, grid) and grid[nx][ny] == current_height + 1:
            path_count += dfs_count_paths(nx, ny, grid, current_height + 1, visited)

    visited.remove((x, y))  # Backtrack

    return path_count


def calculate_total_trailhead_ratings(grid):
    """
    Calculate the total ratings for all trailheads in the grid.
    """
    total_rating = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:  # Found a trailhead
                visited = set()
                total_rating += dfs_count_paths(x, y, grid, 0, visited)

    return total_rating


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python hiking_trail_ratings.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Parse the topographic map
        grid = parse_map(input_file)

        # Calculate total ratings of all trailheads
        total_rating = calculate_total_trailhead_ratings(grid)

        print(f"The sum of the ratings of all trailheads is: {total_rating}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
