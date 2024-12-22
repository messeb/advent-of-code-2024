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


def simulate_buyer(initial_secret, iterations=2000):
    """Simulate the sequence of secret numbers for a buyer."""
    secret = initial_secret
    for _ in range(iterations):
        secret = next_secret(secret)
    return secret


def main(input_file):
    # Read the initial secret numbers from the input file
    with open(input_file, 'r') as f:
        initial_secrets = [int(line.strip()) for line in f if line.strip()]

    # Simulate each buyer and calculate the sum of the 2000th secret numbers
    total = sum(simulate_buyer(secret) for secret in initial_secrets)

    print(f"Total sum of the 2000th secret numbers: {total}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 monkey_market.py input.txt")
        sys.exit(1)

    main(sys.argv[1])
