import re

def extract_and_sum_mul_with_conditions(memory):
    """
    Scans the memory string for valid `mul(X,Y)` instructions
    and sums up their results, taking into account `do()` and `don't()` conditions.
    """
    # Regular expressions for parsing
    mul_pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    condition_pattern = r"(do\(\)|don't\(\))"

    # Track enabled/disabled state for `mul` instructions
    enabled = True
    total_sum = 0

    # Iterate through the memory looking for conditions and valid `mul` instructions
    position = 0
    while position < len(memory):
        # Search for the next condition or `mul` instruction
        condition_match = re.search(condition_pattern, memory[position:])
        mul_match = re.search(mul_pattern, memory[position:])

        # Determine the next relevant instruction
        if condition_match and (not mul_match or condition_match.start() < mul_match.start()):
            condition = condition_match.group()
            enabled = condition == "do()"
            position += condition_match.end()
        elif mul_match:
            if enabled:
                x, y = map(int, mul_match.groups())
                total_sum += x * y
            position += mul_match.end()
        else:
            break

    return total_sum

def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python mull_it_over_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Read the corrupted memory input from the file
        with open(file_path, 'r') as file:
            memory = file.read()

        # Extract and sum valid `mul` instructions with conditions
        result = extract_and_sum_mul_with_conditions(memory)
        print(f"The sum of all enabled `mul` instructions is: {result}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
