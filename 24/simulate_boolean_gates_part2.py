import sys
from collections import defaultdict


def read_input(input_file):
    """
    Read and parse the input file into wires and gates.
    """
    with open(input_file, "r") as f:
        content = f.read()
    wires_data, joints_data = content.split("\n\n")
    wires = {line[:3]: int(line[5]) for line in wires_data.splitlines()}
    gates = [(line.split(), output) for line, output in (gate.split(" -> ") for gate in joints_data.splitlines())]
    return wires, gates


def swap(a, b, pairs, gates):
    """
    Swap the outputs of gates `a` and `b`.
    """
    pairs.append((a, b))
    for i, (inputs, output) in enumerate(gates):
        if output in (a, b):
            gates[i] = (inputs, next(j for j in (a, b) if j != output))


def initialize_lookups(gates):
    """
    Initialize lookup and reverse lookup dictionaries.
    """
    lookup = {output: (a, op, b) for (a, op, b), output in gates}
    reverse_lookup = defaultdict(str, {frozenset(inputs): output for (inputs, output) in gates})
    return lookup, reverse_lookup


def locate_adder_and_carry(reverse_lookup):
    """
    Locate the adder and carry gates for the initial position.
    """
    adder = reverse_lookup[frozenset(("x00", "XOR", "y00"))]
    carry = reverse_lookup[frozenset(("x00", "AND", "y00"))]
    return adder, carry


def process_bit_position(xi, yi, zi, reverse_lookup, lookup, carry, pairs, gates):
    """
    Process a single bit position and handle swaps if necessary.
    """
    bit = reverse_lookup[frozenset((xi, "XOR", yi))]
    adder = reverse_lookup[frozenset((bit, "XOR", carry))]

    if adder:
        c1 = reverse_lookup[frozenset((xi, "AND", yi))]
        c2 = reverse_lookup[frozenset((bit, "AND", carry))]
        carry = reverse_lookup[frozenset((c1, "OR", c2))]
    else:
        a, op, b = lookup[zi]
        swap(bit, next(n for n in (a, b) if n != carry), pairs, gates)
        return False, carry

    if adder != zi:
        swap(adder, zi, pairs, gates)
        return False, carry

    return True, carry


def process_gate_swaps(num_z, lookup, reverse_lookup, pairs, gates):
    """
    Process the swaps for all bit positions in the circuit.
    """
    adder, carry = locate_adder_and_carry(reverse_lookup)

    for i in range(1, num_z):
        xi, yi, zi = f"x{i:02}", f"y{i:02}", f"z{i:02}"
        success, carry = process_bit_position(xi, yi, zi, reverse_lookup, lookup, carry, pairs, gates)
        if not success:
            return False

    return True


def simulate_system(wires, gates):
    """
    Simulate the circuit system to find swapped gates.
    """
    pairs = []
    num_z = sum(output.startswith("z") for _, output in gates)
    lookup, reverse_lookup = initialize_lookups(gates)

    while len(pairs) < 4:
        # Ensure references are consistent for each iteration
        lookup, reverse_lookup = initialize_lookups(gates)
        success = process_gate_swaps(num_z, lookup, reverse_lookup, pairs, gates)
        if not success:
            continue

    # Return sorted swapped gates
    return sorted([gate for pair in pairs for gate in pair])


def main():
    """
    Main function to read input and simulate the system.
    """
    if len(sys.argv) != 2:
        print("Usage: python simulate_boolean_gates.py input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    wires, gates = read_input(input_file)
    swapped_gates = simulate_system(wires, gates)
    print(*swapped_gates, sep=",")


if __name__ == "__main__":
    main()
