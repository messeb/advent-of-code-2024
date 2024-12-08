from itertools import combinations


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


def calculate_harmonic_antinodes(grid, antennas):
    """
    Calculate all unique antinode positions within the grid bounds, considering resonant harmonics.
    """
    rows, cols = len(grid), len(grid[0])
    antinode_positions = set()

    for frequency, positions in antennas.items():
        # Every antenna is an antinode
        for pos in positions:
            antinode_positions.add(pos)

        if len(positions) < 2:
            continue

        # Check all pairs of antennas for collinear positions
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            dr, dc = r2 - r1, c2 - c1
            gcd = abs(dr) if dc == 0 else abs(dc) if dr == 0 else abs(__import__("math").gcd(dr, dc))
            dr //= gcd
            dc //= gcd

            # Step in both directions to find collinear points
            r, c = r1 - dr, c1 - dc
            while 0 <= r < rows and 0 <= c < cols:
                antinode_positions.add((r, c))
                r -= dr
                c -= dc

            r, c = r2 + dr, c2 + dc
            while 0 <= r < rows and 0 <= c < cols:
                antinode_positions.add((r, c))
                r += dr
                c += dc

    return antinode_positions


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python resonant_collinearity_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the input map
        grid, antennas = parse_map(file_path)

        # Calculate unique antinode positions considering resonant harmonics
        antinodes = calculate_harmonic_antinodes(grid, antennas)

        # Print the result
        print(f"The total number of unique antinode locations is: {len(antinodes)}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
