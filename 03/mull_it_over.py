import re

def extract_and_sum_mul_instructions(memory):
    """
    Scans the memory string for valid `mul(X,Y)` instructions
    and sums up their results.
    """
    # Regular expression to match valid `mul(X,Y)` instructions
    pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    
    # Find all matches in the memory string
    matches = re.findall(pattern, memory)
    
    # Calculate the sum of all valid multiplications
    total_sum = sum(int(x) * int(y) for x, y in matches)
    
    return total_sum

def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python mull_it_over.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Read the corrupted memory input from the file
        with open(file_path, 'r') as file:
            memory = file.read()

        # Extract and sum valid `mul` instructions
        result = extract_and_sum_mul_instructions(memory)
        print(f"The sum of all valid `mul` instructions is: {result}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
