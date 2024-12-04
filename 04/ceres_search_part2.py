import sys

# Global grid and dimensions
grid = []
rows, cols = 0, 0


def is_valid_position(x, y):
    """
    Check if the given position (x, y) is within the grid bounds.
    """
    return 0 <= x < rows and 0 <= y < cols


def check_diagonal(x, y, primary_diagonal, secondary_diagonal):
    """
    Check a single diagonal for an X-MAS pattern.

    Parameters:
    - x, y: Center position (must be 'A').
    - primary_diagonal: Tuple for the first arm's direction (x_offset, y_offset).
    - secondary_diagonal: Tuple for the second arm's direction (x_offset, y_offset).

    Returns:
    - 1 if the diagonal forms a valid X-MAS leg, 0 otherwise.
    """
    x1, y1 = x + primary_diagonal[0], y + primary_diagonal[1]  # First diagonal arm
    x2, y2 = x + secondary_diagonal[0], y + secondary_diagonal[1]  # Second diagonal arm

    # Check if both positions are valid
    if not (is_valid_position(x1, y1) and is_valid_position(x2, y2)):
        return 0

    # Check for 'M ↔ S' or 'S ↔ M' pattern
    if (grid[x1][y1] == 'M' and grid[x2][y2] == 'S') or (grid[x1][y1] == 'S' and grid[x2][y2] == 'M'):
        return 1

    return 0


def count_x_mas_at(x, y):
    """
    Check for an X-MAS pattern centered at grid[x][y].

    An X-MAS pattern requires:
    - The center to be 'A'.
    - Two valid diagonal legs (top-left ↔ bottom-right, top-right ↔ bottom-left).
    """
    if grid[x][y] != "A":
        return 0  # Center must be 'A'

    # Define diagonal directions
    diagonals = [
        ((-1, -1), (1, 1)),  # Top-left ↔ Bottom-right
        ((-1, 1), (1, -1))   # Top-right ↔ Bottom-left
    ]

    # Count the number of valid diagonal legs
    valid_legs = sum(check_diagonal(x, y, primary_diagonal, secondary_diagonal) for primary_diagonal, secondary_diagonal in diagonals)

    # If both diagonal legs are valid, it's an X-MAS pattern
    return 1 if valid_legs == 2 else 0


def count_total_x_mas():
    """
    Count all X-MAS patterns in the grid by checking every cell as a potential center.
    """
    total_count = 0
    for x in range(rows):
        for y in range(cols):
            total_count += count_x_mas_at(x, y)
    return total_count


def main():
    global grid, rows, cols

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python ceres_search_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Read the word search grid from the file
        with open(file_path, 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]

        # Update global dimensions
        rows, cols = len(grid), len(grid[0])

        # Count all occurrences of X-MAS
        result = count_total_x_mas()
        print(f"The X-MAS pattern appears {result} times in the word search.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
