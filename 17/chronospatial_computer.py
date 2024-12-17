import sys

def parse_input(filename):
    """Parses the input file to extract registers and program instructions."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    A = B = C = None
    program = []

    for line in lines:
        if line.startswith("Register A:"):
            A = int(line.split(":")[1].strip())
        elif line.startswith("Register B:"):
            B = int(line.split(":")[1].strip())
        elif line.startswith("Register C:"):
            C = int(line.split(":")[1].strip())
        elif line.startswith("Program:"):
            program = [int(x) for x in line.split(":")[1].split(",")]

    return A, B, C, program

def combo_value(op, a, b, c):
    """Calculates the combo operand value."""
    return op if op < 4 else {4: a, 5: b, 6: c}[op]

def run_program(a, arr):
    """
    Simulates the program using the given 'a' as input.
    Implements the provided algorithm logic to compute outputs.
    """
    b = c = 0
    n = len(arr)
    i = 0
    out = []

    while i < n - 1:
        code, op = arr[i], arr[i + 1]
        i += 2

        if code == 0:  # adv
            a //= pow(2, combo_value(op, a, b, c))
        elif code == 1:  # bxl
            b ^= op
        elif code == 2:  # bst
            b = combo_value(op, a, b, c) % 8
        elif code == 3:  # jnz
            if a != 0:
                i = op
        elif code == 4:  # bxc
            b ^= c
        elif code == 5:  # out
            out.append(combo_value(op, a, b, c) % 8)
        elif code == 6:  # bdv
            b = a // pow(2, combo_value(op, a, b, c))
        elif code == 7:  # cdv
            c = a // pow(2, combo_value(op, a, b, c))
    return out

def find_alternative_A(arr):
    """
    Implements the reverse-engineering logic to find an alternative A.
    Starts from the end and reconstructs valid A values.
    """
    ans = [0]
    for i in range(len(arr)):
        ans = [n * 8 + a for n in ans for a in range(8) if arr[-i - 1:] == run_program(n * 8 + a, arr)]
    return ans[0]

def main():
    if len(sys.argv) != 2:
        print("Usage: python chronospatial_computer.py input.txt")
        sys.exit(1)

    # Parse input
    filename = sys.argv[1]
    A, B, C, program = parse_input(filename)

    # Step 1: Run the program with the original A
    original_output = run_program(A, program)
    print(f"Original A: {A}")
    print(f"Program output: {','.join(map(str, original_output))}")

    # Step 2: Find an alternative A that reproduces the same output
    alternative_A = find_alternative_A(program)
    print(f"Alternative A: {alternative_A}")

if __name__ == "__main__":
    main()
