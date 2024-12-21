import sys
from collections import defaultdict, deque

INFINITY = float('inf')

class CustomDict(dict):
    """Custom dictionary class for graph representation."""
    pass


# Graph for numeric keypad
numeric_keypad = CustomDict({
    'A': [('0', '<'), ('3', '^')],
    '0': [('A', '>'), ('2', '^')],
    '1': [('2', '>'), ('4', '^')],
    '2': [('0', 'v'), ('1', '<'), ('3', '>'), ('5', '^')],
    '3': [('A', 'v'), ('2', '<'), ('6', '^')],
    '4': [('1', 'v'), ('5', '>'), ('7', '^')],
    '5': [('2', 'v'), ('4', '<'), ('6', '>'), ('8', '^')],
    '6': [('3', 'v'), ('5', '<'), ('9', '^')],
    '7': [('4', 'v'), ('8', '>')],
    '8': [('5', 'v'), ('7', '<'), ('9', '>')],
    '9': [('6', 'v'), ('8', '<')],
})
numeric_keypad.name = 'numeric_keypad'

# Graph for directional keypad
directional_keypad = CustomDict({
    'A': [('>', 'v'), ('^', '<')],
    '^': [('A', '>'), ('v', 'v')],
    '<': [('v', '>')],
    '>': [('v', '<'), ('A', '^')],
    'v': [('<', '<'), ('>', '>'), ('^', '^')],
})
directional_keypad.name = 'directional_keypad'

# Global memoization dictionary
memoization = {}


def bfs_all_paths(graph, src, dst):
    """Breadth-first search to find all shortest paths."""
    queue = deque([(src, '')])
    distance = defaultdict(lambda: INFINITY, {src: 0})
    paths = []

    while queue:
        node, path = queue.popleft()
        if node == dst:
            if len(path) <= distance[dst]:
                paths.append(path)
            continue

        for neighbor, key in graph[node]:
            d = distance[node] + 1
            if d > distance[dst] or d > distance[neighbor]:
                continue

            distance[neighbor] = d
            queue.append((neighbor, path + key))

    assert len(set(map(len, paths))) == 1
    return paths


def solve(graph_name, code, robots, curchar='A'):
    """Recursive function to calculate steps to type a code."""
    global memoization

    key = (graph_name, code, robots, curchar)
    if key in memoization:
        return memoization[key]

    graph = directional_keypad if graph_name == 'directional_keypad' else numeric_keypad
    if not code:
        return 0

    if robots == 0:
        # Follow any shortest path as is
        total_steps = 0
        for a, b in zip(curchar + code, code):
            total_steps += len(bfs_all_paths(graph, a, b)[0]) + 1
        memoization[key] = total_steps
        return total_steps

    # Explore all paths from current character to next
    nextchar = code[0]
    paths = bfs_all_paths(graph, curchar, nextchar)

    best = INFINITY
    for path in paths:
        robot_steps = solve('directional_keypad', path + 'A', robots - 1)
        best = min(best, robot_steps)

    result = best + solve(graph.name, code[1:], robots, nextchar)
    memoization[key] = result
    return result


def parse_input(filepath):
    """Parse input codes from a file."""
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def calculate_total(parsed, robot_count):
    """Calculate the total complexity."""
    global memoization
    memoization.clear()
    total = 0

    for code in parsed:
        steps = solve('numeric_keypad', code, robot_count)
        numeric_part = int(code[:-1])  # Extract numeric part (ignoring the last character)
        total += numeric_part * steps

    return total


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 keypad_solution.py input.txt")
        sys.exit(1)

    filepath = sys.argv[1]
    codes = parse_input(filepath)

    # Part 1
    result_part1 = calculate_total(codes, 2)
    print(f"Part 1: {result_part1}")

    # Part 2
    result_part2 = calculate_total(codes, 25)
    print(f"Part 2: {result_part2}")


if __name__ == "__main__":
    main()
