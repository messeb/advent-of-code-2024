def parse_disk_map(disk_map):
    """
    Parse the dense disk map into a list of file IDs and free spaces.
    Each digit alternates between file lengths and free space lengths.
    """
    parsed_map = []
    is_free_space = False
    file_id = 0

    for char in disk_map:
        length = int(char)
        if is_free_space:
            parsed_map.extend(['.'] * length)  # Free space
        else:
            parsed_map.extend([file_id] * length)  # File blocks
            file_id += 1
        is_free_space = not is_free_space

    return parsed_map


def compact_disk(parsed_map):
    """
    Compact the disk by moving the last number to the leftmost free space.
    """
    left_index = 0
    right_index = len(parsed_map) - 1

    # Move blocks until indices cross
    while left_index < right_index:
        if parsed_map[left_index] == '.':  # Found a free space
            while parsed_map[right_index] == '.' and right_index > left_index:
                right_index -= 1  # Skip trailing free spaces
            if left_index < right_index:
                # Move the block to the free space
                parsed_map[left_index] = parsed_map[right_index]
                parsed_map[right_index] = '.'
                right_index -= 1
        left_index += 1

    return parsed_map


def calculate_checksum(compacted_map):
    """
    Calculate the checksum for the compacted disk.
    The checksum is the sum of position * file ID for all file blocks.
    """
    checksum = 0
    for position, block in enumerate(compacted_map):
        if block != '.':  # Only consider file blocks
            checksum += position * block
    return checksum


def main():
    import sys

    # Ensure the user provides a file path
    if len(sys.argv) != 2:
        print("Usage: python disk_fragmenter.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            disk_map = file.read().strip()

        # Parse the disk map
        parsed_map = parse_disk_map(disk_map)

        # Compact the disk
        compacted_map = compact_disk(parsed_map)

        # Calculate and print the checksum
        checksum = calculate_checksum(compacted_map)
        print(f"The resulting filesystem checksum is: {checksum}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
