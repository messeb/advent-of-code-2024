from collections import Counter
import sys

def calculate_similarity_score_from_file(file_path):
    """
    Reads pairs of numbers from a file, calculates the total similarity score
    by multiplying each number in the left list by the number of times it appears in the right list.
    """
    left_list = []
    right_list = []
    
    # Read the file and populate the lists
    with open(file_path, 'r') as file:
        for line in file:
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
    
    # Count occurrences in the right list
    right_count = Counter(right_list)
    
    # Calculate the similarity score
    similarity_score = sum(left * right_count[left] for left in left_list)
    
    return similarity_score

def main():
    # Ensure the user provided a file path as an argument
    if len(sys.argv) != 2:
        print("Usage: python calculate_similarity_score.py <input_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # Calculate the similarity score
        similarity_score = calculate_similarity_score_from_file(file_path)
        print(f"The similarity score between the two lists is: {similarity_score}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
