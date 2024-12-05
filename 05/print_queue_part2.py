from collections import defaultdict, deque

def parse_input(file_path):
    """
    Parse the input file into rules and updates.

    Parameters:
    - file_path: Path to the input file.

    Returns:
    - rules: List of tuples representing ordering rules.
    - updates: List of lists representing each update.
    """
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    # Separate rules and updates
    rules = []
    updates = []
    is_update_section = False

    for line in lines:
        if ',' in line:
            # Update section begins
            updates.append(list(map(int, line.split(','))))
            is_update_section = True
        elif '|' in line:
            # Rules section
            rules.append(tuple(map(int, line.split('|'))))

    return rules, updates


def is_update_ordered(update, rules):
    """
    Check if an update is in the correct order according to the rules.

    Parameters:
    - update: List of integers representing the pages in the update.
    - rules: List of tuples representing ordering rules.

    Returns:
    - True if the update is ordered correctly, False otherwise.
    """
    page_positions = {page: pos for pos, page in enumerate(update)}
    
    for before, after in rules:
        if before in page_positions and after in page_positions:
            if page_positions[before] > page_positions[after]:
                return False
    return True


def reorder_update(update, rules):
    """
    Reorder an update to follow the given rules.

    Parameters:
    - update: List of integers representing the pages in the update.
    - rules: List of tuples representing ordering rules.

    Returns:
    - List of integers representing the reordered update.
    """
    # Build a directed graph of the rules
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Filter rules to only include relevant pages in this update
    relevant_rules = [(before, after) for before, after in rules if before in update and after in update]
    pages = set(update)
    
    for before, after in relevant_rules:
        graph[before].append(after)
        in_degree[after] += 1
        in_degree.setdefault(before, 0)  # Ensure all nodes are in the in_degree map

    # Topological sort using Kahn's algorithm
    sorted_pages = []
    queue = deque(page for page in pages if in_degree[page] == 0)

    while queue:
        current = queue.popleft()
        sorted_pages.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_pages


def find_middle_page(update):
    """
    Find the middle page number of an update.

    Parameters:
    - update: List of integers representing the pages in the update.

    Returns:
    - The middle page number.
    """
    return update[len(update) // 2]


def main():
    import sys

    # Ensure the user provides a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python print_queue_part2.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse input file
        rules, updates = parse_input(file_path)

        # Process updates
        incorrectly_ordered_updates = [
            update for update in updates if not is_update_ordered(update, rules)
        ]

        # Reorder the incorrect updates
        reordered_updates = [reorder_update(update, rules) for update in incorrectly_ordered_updates]

        # Find middle page numbers and compute their sum
        middle_pages = [find_middle_page(update) for update in reordered_updates]
        result = sum(middle_pages)

        print(f"The sum of the middle page numbers from correctly-reordered updates is: {result}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
