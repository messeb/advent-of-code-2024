import sys

def count_xmas_occurrences(grid):
    """
    Counts all occurrences of the word "XMAS" in the word search grid.
    Words can be horizontal, vertical, diagonal, backwards, and overlapping.
    """
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols

    def check_direction(x, y, dx, dy):
        for i in range(len(word)):
            if not is_valid(x + i * dx, y + i * dy) or grid[x + i * dx][y + i * dy] != word[i]:
                return False
        return True

    word = "XMAS"
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions
    count = 0

    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                if check_direction(x, y, dx, dy):
                    count += 1
    return count


def main():
    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python ceres_search.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Read the word search grid from the file
        with open(file_path, 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]

        # Count all occurrences of "XMAS"
        result = count_xmas_occurrences(grid)
        print(f"The word 'XMAS' appears {result} times in the word search.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
