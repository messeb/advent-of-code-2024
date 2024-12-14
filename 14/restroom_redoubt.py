import sys

def parse_line(line):
    # Each line: p=x,y v=dx,dy
    # Example: "p=0,4 v=3,-3"
    parts = line.strip().split()
    # parts[0] like "p=0,4"
    # parts[1] like "v=3,-3"

    # Parse position p
    p_str = parts[0][2:]  # remove "p="
    px_str, py_str = p_str.split(',')
    x = int(px_str)
    y = int(py_str)

    # Parse velocity v
    v_str = parts[1][2:]  # remove "v="
    vx_str, vy_str = v_str.split(',')
    vx = int(vx_str)
    vy = int(vy_str)

    return x, y, vx, vy

def simulate(robots, width, height, seconds):
    # Update each robot's position after `seconds` seconds with wrap-around.
    updated_robots = []
    for (x, y, vx, vy) in robots:
        new_x = (x + vx*seconds) % width
        new_y = (y + vy*seconds) % height
        updated_robots.append((new_x, new_y))
    return updated_robots

def count_quadrants(positions, mid_x, mid_y):
    # Count how many robots appear in each quadrant after filtering out
    # those on the mid lines.
    q1 = q2 = q3 = q4 = 0
    for (x, y) in positions:
        if x == mid_x or y == mid_y:
            continue
        if x > mid_x and y < mid_y:
            q1 += 1
        elif x < mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1
    return q1, q2, q3, q4

def main():
    if len(sys.argv) != 2:
        print("Usage: python restroom_redoubt.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Dimensions as stated in the problem
    width = 101
    height = 103
    mid_x = 50
    mid_y = 51

    robots = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    x, y, vx, vy = parse_line(line)
                    robots.append((x, y, vx, vy))
    except FileNotFoundError:
        print(f"Error: file '{input_file}' not found.")
        sys.exit(1)

    # Simulate 100 seconds
    seconds = 100
    final_positions = simulate(robots, width, height, seconds)

    # Count quadrants
    q1, q2, q3, q4 = count_quadrants(final_positions, mid_x, mid_y)

    # Compute safety factor
    safety_factor = q1 * q2 * q3 * q4
    print(safety_factor)

if __name__ == "__main__":
    main()
