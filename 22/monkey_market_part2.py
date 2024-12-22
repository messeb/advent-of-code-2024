from collections import defaultdict


def mix_and_prune(secret, value):
    """Mix a value into the secret number and prune it."""
    secret ^= value  # Mix with XOR
    secret %= 16777216  # Prune with modulo
    return secret


def next_secret(secret):
    """Generate the next secret number based on the rules."""
    # Step 1: Multiply by 64, mix, prune
    secret = mix_and_prune(secret, secret * 64)

    # Step 2: Divide by 32 (rounded down), mix, prune
    secret = mix_and_prune(secret, secret // 32)

    # Step 3: Multiply by 2048, mix, prune
    secret = mix_and_prune(secret, secret * 2048)

    return secret


def simulate_and_find_best_sequence(buyers, iterations=2000):
    """Simulate prices and find the best sequence of 4 price changes."""
    sequence_totals = defaultdict(int)  # Map sequence -> total bananas
    max_bananas = 0
    best_sequence = None

    for buyer in buyers:
        secret = buyer
        prices = []
        price_changes = []
        first_occurrence = set()  # Track sequences already matched for this buyer

        # Generate prices and price changes
        for _ in range(iterations):
            secret = next_secret(secret)
            price = secret % 10
            if prices:
                price_changes.append(price - prices[-1])
            prices.append(price)

            # Check for sequences after we have 4 changes
            if len(price_changes) >= 4:
                sequence = tuple(price_changes[-4:])
                if sequence not in first_occurrence:
                    first_occurrence.add(sequence)
                    sequence_totals[sequence] += price

    # Find the best sequence
    for sequence, bananas in sequence_totals.items():
        if bananas > max_bananas:
            max_bananas = bananas
            best_sequence = sequence

    return best_sequence, max_bananas


def main(input_file):
    # Read the initial secret numbers from the input file
    with open(input_file, 'r') as f:
        buyers = [int(line.strip()) for line in f if line.strip()]

    best_sequence, max_bananas = simulate_and_find_best_sequence(buyers)

    print(f"The best sequence of changes is: {best_sequence}")
    print(f"The maximum bananas you can get: {max_bananas}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 monkey_market_part2_corrected.py input.txt")
        sys.exit(1)

    main(sys.argv[1])
