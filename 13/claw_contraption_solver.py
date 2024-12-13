import sys

def solve_machine(Ax, Ay, Bx, By, Px, Py):
    """
    Solve the system:
        Ax*a + Bx*b = Px
        Ay*a + By*b = Py
    for nonnegative integers (a,b).
    If a solution exists, return minimal cost = 3*a + b.
    Otherwise, return None.
    """
    det = Ax*By - Ay*Bx
    if det == 0:
        return None  # No unique solution

    num_a = Px*By - Py*Bx
    num_b = Ax*Py - Ay*Px

    if num_a % det != 0 or num_b % det != 0:
        # Not an integer solution
        return None

    a0 = num_a // det
    b0 = num_b // det

    # Check non-negativity
    if a0 < 0 or b0 < 0:
        return None

    cost = 3*a0 + b0
    return cost

def parse_line(line):
    # Parse a line like "Button A: X+94, Y+34" or "Prize: X=8400, Y=5400"
    line = line.strip()
    parts = line.split(':')
    coords_part = parts[1].strip()
    coords = coords_part.split(',')
    x_part = coords[0].strip()
    y_part = coords[1].strip()

    def extract_val(s):
        s = s[1:]  # remove 'X' or 'Y'
        s = s.replace('=', '+')  # turn "X=8400" into "X+8400" after removal of 'X'
        return int(s)

    x_val = extract_val(x_part)
    y_val = extract_val(y_part)
    return x_val, y_val

def main():
    if len(sys.argv) != 3:
        print("Usage: python claw_contraption_solver.py <input_file> <offset>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        offset = int(sys.argv[2])
    except ValueError:
        print("Offset must be an integer.")
        sys.exit(1)

    try:
        with open(input_file, 'r') as f:
            lines = [line for line in f if line.strip()]

        if len(lines) % 3 != 0:
            print("Input format error: number of lines is not a multiple of 3.")
            sys.exit(1)

        machines = []
        for i in range(0, len(lines), 3):
            a_line = lines[i]
            b_line = lines[i+1]
            p_line = lines[i+2]

            Ax, Ay = parse_line(a_line)
            Bx, By = parse_line(b_line)
            Px, Py = parse_line(p_line)

            # Add the user-specified offset to the prize coordinates
            Px += offset
            Py += offset

            machines.append((Ax, Ay, Bx, By, Px, Py))

        costs = []
        for (Ax, Ay, Bx, By, Px, Py) in machines:
            cost = solve_machine(Ax, Ay, Bx, By, Px, Py)
            costs.append(cost)

        solvable_costs = [c for c in costs if c is not None]

        print("Number of prizes won:", len(solvable_costs))
        print("Fewest tokens spent:", sum(solvable_costs))

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
