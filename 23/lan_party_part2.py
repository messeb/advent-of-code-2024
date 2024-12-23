import sys
from collections import defaultdict, deque

def parse_input(file_path):
    """Parses the input file and returns a dictionary of connections."""
    connections = defaultdict(set)
    with open(file_path, 'r') as f:
        for line in f:
            a, b = line.strip().split('-')
            connections[a].add(b)
            connections[b].add(a)
    return connections

def find_largest_clique(connections):
    """Finds the largest set of fully connected computers using a graph traversal approach."""
    visited = set()
    max_clique = []

    def bfs_clique(node):
        """Perform BFS to find cliques starting from a given node."""
        queue = deque([node])
        clique = set([node])
        while queue:
            current = queue.popleft()
            for neighbor in connections[current]:
                if neighbor not in clique and all(neighbor in connections[n] for n in clique):
                    clique.add(neighbor)
                    queue.append(neighbor)
        return clique

    for node in connections:
        if node not in visited:
            clique = bfs_clique(node)
            visited.update(clique)
            if len(clique) > len(max_clique):
                max_clique = clique

    return sorted(max_clique)

def main():
    if len(sys.argv) != 2:
        print("Usage: python lan_party_triples.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        connections = parse_input(input_file)

        # Part 2: Find the largest clique
        largest_clique = find_largest_clique(connections)
        password = ','.join(largest_clique)

        print("\nLargest fully connected set (LAN Party):", password)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
