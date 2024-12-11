from collections import Counter

def transform_stone(stone):
    """
    Transform a single stone according to the rules:
    - If the number is 0, replace it with 1.
    - If the number has an even number of digits, split it into two stones.
    - Otherwise, multiply the number by 2024.
    """
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        mid = len(str(stone)) // 2
        left = int(str(stone)[:mid])
        right = int(str(stone)[mid:])
        return [left, right]
    else:
        return [stone * 2024]

def simulate_blinks_optimized(initial_stones, blinks):
    """
    Simulate the transformations for the given number of blinks using an optimized approach.

    Args:
        initial_stones (list of int): Initial stone numbers.
        blinks (int): Number of blinks to simulate.

    Returns:
        int: Number of stones after the given number of blinks.
    """
    current_state = Counter(initial_stones)

    for _ in range(blinks):
        next_state = Counter()
        for stone, count in current_state.items():
            transformed = transform_stone(stone)
            for new_stone in transformed:
                next_state[new_stone] += count
        current_state = next_state

    return sum(current_state.values())

def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python plutonian_pebbles.py <input_file> <blinks>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        blinks = int(sys.argv[2])
    except ValueError:
        print("Error: Blinks must be an integer.")
        sys.exit(1)

    try:
        with open(input_file, 'r') as file:
            initial_stones = list(map(int, file.read().strip().split()))

        result = simulate_blinks_optimized(initial_stones, blinks)

        print(f"After {blinks} blinks, there are {result} stones.")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()