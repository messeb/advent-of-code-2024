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


def simulate_with_obstacle(grid, start_position, start_direction, obstacle):
    """
    Simulate the guard's patrol with an added obstacle to check for loops.

    Parameters:
    - grid: The lab map as a list of lists.
    - start_position: The initial position of the guard as (row, col).
    - start_direction: The initial direction of the guard as (row_offset, col_offset).
    - obstacle: The position (row, col) of the added obstacle.

    Returns:
    - True if the guard gets stuck in a loop, False otherwise.
    """
    rows, cols = len(grid), len(grid[0])
    current_position = start_position
    current_direction = start_direction
    visited_states = set()

    # Add the obstacle to the grid temporarily
    grid[obstacle[0]][obstacle[1]] = '#'

    while True:
        # Save the current state (position and direction) to detect loops
        state = (current_position, current_direction)
        if state in visited_states:
            # The guard is stuck in a loop
            grid[obstacle[0]][obstacle[1]] = '.'  # Restore the grid
            return True
        visited_states.add(state)

        x, y = current_position
        next_position = (x + current_direction[0], y + current_direction[1])

        # Check if the next position is out of bounds
        if not (0 <= next_position[0] < rows and 0 <= next_position[1] < cols):
            grid[obstacle[0]][obstacle[1]] = '.'  # Restore the grid
            return False

        # Check if the next position is obstructed
        if grid[next_position[0]][next_position[1]] == '#':
            # Turn right if there's an obstacle
            current_direction = turn_right(current_direction)
        else:
            # Move forward
            current_position = next_position


def find_loop_causing_positions(grid, start_position, start_direction):
    """
    Find all positions where adding an obstacle would cause the guard to get stuck in a loop.

    Parameters:
    - grid: The lab map as a list of lists.
    - start_position: The initial position of the guard as (row, col).
    - start_direction: The initial direction of the guard as (row_offset, col_offset).

    Returns:
    - A set of all positions (row, col) that would cause a loop.
    """
    rows, cols = len(grid), len(grid[0])
    loop_positions = set()

    for x in range(rows):
        for y in range(cols):
            # Skip if the position is already obstructed or is the guard's starting position
            if grid[x][y] == '#' or (x, y) == start_position:
                continue

            # Check if adding an obstacle here causes a loop
            if simulate_with_obstacle(grid, start_position, start_direction, (x, y)):
                loop_positions.add((x, y))

    return loop_positions


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python guard_patrol_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the input map
        grid, start_position, start_direction = parse_map(file_path)

        # Find all loop-causing positions
        loop_positions = find_loop_causing_positions(grid, start_position, start_direction)

        # Output the result
        print(f"There are {len(loop_positions)} positions where an obstruction would cause a loop.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
