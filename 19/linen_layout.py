import sys

def parse_input(filename):
    """Parse the input file to extract towel patterns and designs."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    towel_patterns = lines[0].split(", ")
    designs = lines[1:]
    return towel_patterns, designs

def can_form_design_dp(patterns, design):
    """
    Use dynamic programming to determine if a design can be formed.
    Each substring of the design is checked and memoized for faster lookup.
    """
    dp = [False] * (len(design) + 1)
    dp[0] = True  # Base case: an empty design can always be formed.

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i - len(pattern):i] == pattern and dp[i - len(pattern)]:
                dp[i] = True
                break

    return dp[len(design)]

def count_possible_designs(patterns, designs):
    """Count how many designs can be formed using the DP approach."""
    count = 0
    for design in designs:
        if can_form_design_dp(patterns, design):
            count += 1
    return count

def main():
    if len(sys.argv) != 2:
        print("Usage: python linen_layout_optimized.py <input_file>")
        sys.exit(1)

    # Parse the input file
    filename = sys.argv[1]
    towel_patterns, designs = parse_input(filename)

    # Count how many designs are possible
    possible_count = count_possible_designs(towel_patterns, designs)

    print(f"Number of possible designs: {possible_count}")

if __name__ == "__main__":
    main()
