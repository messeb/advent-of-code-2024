def parse_map(file_path):
    """
    Parse the input file to extract the map and locate all antennas with their positions.
    Returns a dictionary with frequencies as keys and lists of (row, col) positions as values.
    """
    antennas = {}
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file]

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char != '.':
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((r, c))
    
    return grid, antennas


def calculate_antinodes(grid, antennas):
    """
    Calculate all unique antinode positions within the grid bounds.
    """
    rows, cols = len(grid), len(grid[0])
    antinode_positions = set()

    for frequency, positions in antennas.items():
        if len(positions) < 2:
            continue

        # Compare all pairs of antennas with the same frequency
        for i, (r1, c1) in enumerate(positions):
            for j, (r2, c2) in enumerate(positions):
                if i >= j:
                    continue

                # Compute potential antinodes
                dr, dc = r2 - r1, c2 - c1

                # Antinode 1 (closer to r1, c1)
                antinode1_r, antinode1_c = r1 - dr, c1 - dc
                if 0 <= antinode1_r < rows and 0 <= antinode1_c < cols:
                    antinode_positions.add((antinode1_r, antinode1_c))

                # Antinode 2 (closer to r2, c2)
                antinode2_r, antinode2_c = r2 + dr, c2 + dc
                if 0 <= antinode2_r < rows and 0 <= antinode2_c < cols:
                    antinode_positions.add((antinode2_r, antinode2_c))

    return antinode_positions


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python resonant_collinearity.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the input map
        grid, antennas = parse_map(file_path)

        # Calculate unique antinode positions
        antinodes = calculate_antinodes(grid, antennas)

        # Print the result
        print(f"The total number of unique antinode locations is: {len(antinodes)}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
