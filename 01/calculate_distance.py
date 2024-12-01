import sys

def calculate_total_distance_from_file(file_path):
    """
    Reads pairs of numbers from a file, sorts the lists,
    and calculates the total distance between paired numbers.
    """
    left_list = []
    right_list = []
    
    # Read the file and populate the lists
    with open(file_path, 'r') as file:
        for line in file:
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
    
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    # Calculate the distance
    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))
    
    return total_distance

def main():
    # Ensure the user provided a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python calculate_distance.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # Calculate the total distance
        total_distance = calculate_total_distance_from_file(file_path)
        print(f"The total distance between the two lists is: {total_distance}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
