from itertools import product

def parse_input(file_path):
    """
    Parse the input file and return the equations as a list of tuples.
    Each tuple contains the target value and a list of numbers.
    """
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                target, numbers = line.split(":")
                target = int(target.strip())
                numbers = list(map(int, numbers.strip().split()))
                equations.append((target, numbers))
    return equations


def evaluate_equation_with_concat(target, numbers):
    """
    Check if any combination of operators can make the numbers produce the target value.
    Operators are evaluated left-to-right without precedence.
    """
    # Number of operators needed for the given numbers
    n_operators = len(numbers) - 1

    # Generate all possible operator combinations (e.g., ['+', '*', '||'])
    for operators in product(['+', '*', '||'], repeat=n_operators):
        # Evaluate the expression left-to-right
        result = numbers[0]
        for i, op in enumerate(operators):
            if op == '+':
                result += numbers[i + 1]
            elif op == '*':
                result *= numbers[i + 1]
            elif op == '||':
                result = int(str(result) + str(numbers[i + 1]))

        # Check if the result matches the target value
        if result == target:
            return True

    return False


def calculate_calibration_result_with_concat(equations):
    """
    Determine the total calibration result by summing the target values of valid equations.
    """
    total_calibration_result = 0
    for target, numbers in equations:
        if evaluate_equation_with_concat(target, numbers):
            total_calibration_result += target
    return total_calibration_result


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python bridge_repair_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse the input file
        equations = parse_input(file_path)

        # Calculate the total calibration result with concatenation
        result = calculate_calibration_result_with_concat(equations)

        print(f"The total calibration result is: {result}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
