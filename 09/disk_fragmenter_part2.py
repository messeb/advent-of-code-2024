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


def find_free_space_spans(disk_map):
    """
    Identify all contiguous spans of free space in the disk map.
    Returns a list of tuples (start_index, length).
    """
    spans = []
    start = None

    for i, block in enumerate(disk_map):
        if block == '.':
            if start is None:
                start = i
        else:
            if start is not None:
                spans.append((start, i - start))
                start = None

    if start is not None:  # Handle trailing free space
        spans.append((start, len(disk_map) - start))

    return spans


def compact_disk_whole_files(parsed_map):
    """
    Compact the disk by moving whole files to the leftmost span of free space
    that can fit them, starting with the highest file ID.
    """
    max_file_id = max(block for block in parsed_map if block != '.')
    for file_id in range(max_file_id, -1, -1):  # Process files by decreasing file ID
        # Find the file's span
        start_index = parsed_map.index(file_id)
        end_index = start_index
        while end_index < len(parsed_map) and parsed_map[end_index] == file_id:
            end_index += 1
        file_length = end_index - start_index

        # Find the leftmost free space span that can fit the file
        free_spans = find_free_space_spans(parsed_map)
        for free_start, free_length in free_spans:
            if free_length >= file_length and free_start < start_index:
                # Move the file
                parsed_map[free_start:free_start + file_length] = [file_id] * file_length
                parsed_map[start_index:end_index] = ['.'] * file_length
                break

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
        print("Usage: python disk_fragmenter_whole_files.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            disk_map = file.read().strip()

        # Parse the disk map
        parsed_map = parse_disk_map(disk_map)

        # Compact the disk by moving whole files
        compacted_map = compact_disk_whole_files(parsed_map)

        # Calculate and print the checksum
        checksum = calculate_checksum(compacted_map)
        print(f"The resulting filesystem checksum is: {checksum}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
