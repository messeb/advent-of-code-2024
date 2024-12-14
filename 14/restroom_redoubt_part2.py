import sys
import re

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

class Grid:
    def __init__(self, robots, width, height):
        self.robots = robots
        self.width = width
        self.height = height
        self.mid_x = 50
        self.mid_y = 51

    def simulate_walks(self, seconds):
        # Update each robot's position after `seconds` with wrap-around.
        updated_robots = []
        for (x, y, vx, vy) in self.robots:
            new_x = (x + vx*seconds) % self.width
            new_y = (y + vy*seconds) % self.height
            updated_robots.append((new_x, new_y))
        return updated_robots

    def count_quadrants(self, positions):
        # Count how many robots appear in each quadrant after filtering out
        # those on the mid lines.
        q1 = q2 = q3 = q4 = 0
        for (x, y) in positions:
            if x == self.mid_x or y == self.mid_y:
                continue
            if x > self.mid_x and y < self.mid_y:
                q1 += 1
            elif x < self.mid_x and y < self.mid_y:
                q2 += 1
            elif x < self.mid_x and y > self.mid_y:
                q3 += 1
            elif x > self.mid_x and y > self.mid_y:
                q4 += 1
        return q1, q2, q3, q4

    def tree_pattern(self):
        # find tree pattern
        '''
        Based on the assumption that the tree pattern is displayed
        when no two robots overlap.
        '''
        seconds = 0
        while True:
            seconds += 1
            positions = self.simulate_walks(seconds)
            if len(positions) == len(set(positions)):
                return seconds


def main():
    if len(sys.argv) != 2:
        print("Usage: python restroom_redoubt.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Dimensions as stated in the problem
    width = 101
    height = 103

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

    # Simulate 100 seconds for Part 1
    seconds = 100
    grid = Grid(robots, width, height)
    final_positions = grid.simulate_walks(seconds)

    # Count quadrants
    q1, q2, q3, q4 = grid.count_quadrants(final_positions)

    # Compute safety factor
    safety_factor = q1 * q2 * q3 * q4
    print(safety_factor)

    # Part 2: Tree pattern
    t = grid.tree_pattern()
    print("Tree pattern found after", t, "seconds")

if __name__ == "__main__":
    main()
