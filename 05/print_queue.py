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
        print("Usage: python print_queue.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        # Parse input file
        rules, updates = parse_input(file_path)

        # Process updates
        correctly_ordered_updates = [
            update for update in updates if is_update_ordered(update, rules)
        ]

        # Find middle page numbers and compute their sum
        middle_pages = [find_middle_page(update) for update in correctly_ordered_updates]
        result = sum(middle_pages)

        print(f"The sum of the middle page numbers from correctly-ordered updates is: {result}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
