def parse_map(file_path):
    """
    Parse the input file to create the map grid and find the guard's initial position and direction.
    """
    with open(file_path, 'r') as file:
        grid = [list(line.strip()) for line in file if line.strip()]

    # Locate the guard's starting position and direction
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    guard_position = None
    guard_direction = None

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in directions:
                guard_position = (row, col)
                guard_direction = directions[grid[row][col]]
                grid[row][col] = '.'  # Clear the guard's initial position for the simulation
                return grid, guard_position, guard_direction

    raise ValueError("No guard (caret) found in the map!")


def turn_right(direction):
    """
    Turn the guard 90 degrees to the right.
    """
    return {
        (-1, 0): (0, 1),   # Up -> Right
        (0, 1): (1, 0),    # Right -> Down
        (1, 0): (0, -1),   # Down -> Left
        (0, -1): (-1, 0)   # Left -> Up
    }[direction]


def simulate_patrol(grid, start_position, start_direction):
    """
    Simulate the guard's patrol and mark visited positions with 'X'.

    Parameters:
    - grid: The lab map as a list of lists.
    - start_position: The initial position of the guard as (row, col).
    - start_direction: The initial direction of the guard as (row_offset, col_offset).

    Returns:
    - The modified grid with visited positions marked as 'X'.
    """
    current_position = start_position
    current_direction = start_direction
    rows, cols = len(grid), len(grid[0])

    while True:
        # Mark the current position as visited
        x, y = current_position
        grid[x][y] = 'X'

        # Determine the next position
        next_position = (x + current_direction[0], y + current_direction[1])

        # Check if the next position is out of bounds
        if not (0 <= next_position[0] < rows and 0 <= next_position[1] < cols):
            # Guard leaves the map
            break

        # Check if the next position is obstructed
        if grid[next_position[0]][next_position[1]] == '#':
            # Turn right if there's an obstacle
            current_direction = turn_right(current_direction)
        else:
            # Move forward
            current_position = next_position

    return grid


def count_visited(grid):
    """
    Count the number of positions marked as 'X' in the grid.
    """
    return sum(row.count('X') for row in grid)


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python guard_patrol.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the input map
        grid, start_position, start_direction = parse_map(file_path)

        # Simulate the guard's patrol
        marked_grid = simulate_patrol(grid, start_position, start_direction)

        # Count the number of visited positions
        visited_count = count_visited(marked_grid)

        print(f"The guard visits {visited_count} distinct positions before leaving the map.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
