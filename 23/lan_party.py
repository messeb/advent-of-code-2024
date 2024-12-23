import sys
from itertools import combinations

def parse_input(file_path):
    """
    Parse the input file to build a map of connections.
    """
    connections = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                a, b = line.strip().split('-')
                connections.append((a, b))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    return connections

def build_adjacency_list(connections):
    """
    Build an adjacency list from the connections.
    """
    adjacency_list = {}
    for a, b in connections:
        if a not in adjacency_list:
            adjacency_list[a] = set()
        if b not in adjacency_list:
            adjacency_list[b] = set()
        adjacency_list[a].add(b)
        adjacency_list[b].add(a)
    return adjacency_list

def find_connected_triplets(adjacency_list):
    """
    Find all sets of three computers where each is connected to the others.
    """
    triplets = set()
    for node, neighbors in adjacency_list.items():
        for pair in combinations(neighbors, 2):
            if pair[0] in adjacency_list[pair[1]]:  # Check if the pair is connected
                triplet = tuple(sorted([node, *pair]))
                triplets.add(triplet)
    return triplets

def filter_triplets_with_t(triplets):
    """
    Filter triplets containing at least one computer whose name starts with 't'.
    """
    return [triplet for triplet in triplets if any(comp.startswith('t') for comp in triplet)]

def main():
    if len(sys.argv) != 2:
        print("Usage: python lan_party.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    connections = parse_input(input_file)
    adjacency_list = build_adjacency_list(connections)
    triplets = find_connected_triplets(adjacency_list)
    filtered_triplets = filter_triplets_with_t(triplets)
    
    print("Total triplets containing at least one 't' computer:", len(filtered_triplets))
    
if __name__ == "__main__":
    main()
