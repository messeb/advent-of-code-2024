import sys
import re

def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    initial_values = {}
    gates = []

    for line in lines:
        if ':' in line:
            wire, value = line.split(':')
            initial_values[wire.strip()] = int(value.strip())
        elif '->' in line:
            gates.append(line.strip())

    return initial_values, gates

def evaluate_gate(value1, operator, value2):
    if operator == "AND":
        return value1 & value2
    elif operator == "OR":
        return value1 | value2
    elif operator == "XOR":
        return value1 ^ value2
    else:
        raise ValueError(f"Unknown operator: {operator}")

def simulate_system(initial_values, gates):
    wire_values = initial_values.copy()
    unresolved_gates = gates[:]

    while unresolved_gates:
        for gate in unresolved_gates[:]:
            match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", gate)
            if match:
                input1, operator, input2, output = match.groups()
                if input1 in wire_values and input2 in wire_values:
                    wire_values[output] = evaluate_gate(wire_values[input1], operator, wire_values[input2])
                    unresolved_gates.remove(gate)

    return wire_values

def compute_output(wire_values):
    z_wires = sorted((key for key in wire_values if key.startswith('z')), key=lambda x: int(x[1:]))
    binary_output = ''.join(str(wire_values[wire]) for wire in z_wires)
    return int(binary_output[::-1], 2)  # Reverse binary string for LSB-to-MSB

def main():
    if len(sys.argv) != 2:
        print("Usage: python simulate_boolean_gates.py input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    initial_values, gates = parse_input(input_file)
    wire_values = simulate_system(initial_values, gates)
    result = compute_output(wire_values)
    print("Decimal output:", result)

if __name__ == "__main__":
    main()
