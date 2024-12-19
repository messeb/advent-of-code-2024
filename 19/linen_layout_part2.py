import sys

def parse_input(filename):
    """Parse the input file to extract towel patterns and designs."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    towel_patterns = lines[0].split(", ")
    designs = lines[1:]
    return towel_patterns, designs

def count_design_arrangements(patterns, design):
    """
    Count the number of ways a design can be formed using dynamic programming.
    dp[i] represents the number of ways to form the first `i` characters of the design.
    """
    dp = [0] * (len(design) + 1)
    dp[0] = 1  # Base case: There's one way to form an empty design (do nothing).

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                dp[i] += dp[i - len(pattern)]

    return dp[len(design)]

def total_arrangements(patterns, designs):
    """Calculate the total number of ways to arrange all designs."""
    total = 0
    for design in designs:
        total += count_design_arrangements(patterns, design)
    return total

def main():
    if len(sys.argv) != 2:
        print("Usage: python linen_layout_part2.py <input_file>")
        sys.exit(1)

    # Parse the input file
    filename = sys.argv[1]
    towel_patterns, designs = parse_input(filename)

    # Count the total number of arrangements
    total = total_arrangements(towel_patterns, designs)

    print(f"Total number of arrangements: {total}")

if __name__ == "__main__":
    main()
