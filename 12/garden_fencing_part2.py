import sys
from collections import deque, defaultdict

def get_neighbors(r, c, rows, cols):
    """Yield the 4-directional neighbors of (r,c)."""
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for dr, dc in directions:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_regions(grid):
    """
    Find all contiguous regions of the same character in the grid.
    Returns a list of regions, where each region is:
    {
      'cells': [(r,c), ...],
      'char': 'X'
    }
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False]*cols for _ in range(rows)]
    regions = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                char = grid[r][c]
                q = deque()
                q.append((r,c))
                visited[r][c] = True
                cells = []
                while q:
                    rr, cc = q.popleft()
                    cells.append((rr, cc))
                    for nr, nc in get_neighbors(rr, cc, rows, cols):
                        if not visited[nr][nc] and grid[nr][nc] == char:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                regions.append({'cells': cells, 'char': char})
    return regions

def compute_sides(grid, region):
    """
    Compute the number of sides for the region:
    1. Identify boundary edges of the region.
    2. Form closed loops from these edges.
    3. Count direction changes to determine how many sides each loop has.
    4. Sum sides from all loops to get the total sides for the region.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    region_cells = set(region['cells'])

    # Identify boundary edges
    # Represent edges as pairs of grid points (corners).
    # Cell (r,c) corners: (r,c), (r,c+1), (r+1,c), (r+1,c+1)
    boundary_edges = []
    for (r,c) in region['cells']:
        # top edge
        if r == 0 or (r-1,c) not in region_cells:
            boundary_edges.append(((r,c),(r,c+1)))
        # bottom edge
        if r == rows-1 or (r+1,c) not in region_cells:
            boundary_edges.append(((r+1,c),(r+1,c+1)))
        # left edge
        if c == 0 or (r,c-1) not in region_cells:
            boundary_edges.append(((r,c),(r+1,c)))
        # right edge
        if c == cols-1 or (r,c+1) not in region_cells:
            boundary_edges.append(((r,c+1),(r+1,c+1)))

    # Build adjacency for edges
    adjacency = defaultdict(list)
    for e in boundary_edges:
        p1, p2 = e
        adjacency[p1].append(p2)
        adjacency[p2].append(p1)

    visited_points = set()
    loops = []

    def find_loop(start):
        loop = []
        current = start
        prev = None
        while True:
            loop.append(current)
            visited_points.add(current)
            neighbors = adjacency[current]
            # Choose the next point that is not the previous one
            if prev is None:
                nextp = neighbors[0]
            else:
                if neighbors[0] == prev:
                    if len(neighbors) > 1:
                        nextp = neighbors[1]
                    else:
                        # Degenerate case: shouldn't occur in well-formed polygons
                        break
                else:
                    nextp = neighbors[0]
            prev, current = current, nextp
            if current == start:
                # loop closed
                break
        return loop

    for point in adjacency:
        if point not in visited_points:
            loops.append(find_loop(point))

    # Count sides in each loop
    def direction(p1, p2):
        return (p2[0]-p1[0], p2[1]-p1[1])

    def count_sides(loop):
        n = len(loop)
        edges = [direction(loop[i], loop[(i+1)%n]) for i in range(n)]
        sides = 1
        for i in range(1, n):
            if edges[i] != edges[i-1]:
                sides += 1
        return sides

    total_sides = sum(count_sides(loop) for loop in loops)
    return total_sides

def calculate_total_fence_price(grid):
    """
    Calculate the total fence price for all regions according to the second problem:
    price per region = area(region) * number_of_sides(region)
    """
    regions = find_regions(grid)
    total_price = 0
    for region in regions:
        area = len(region['cells'])
        sides = compute_sides(grid, region)
        total_price += area * sides
    return total_price

def main():
    if len(sys.argv) != 2:
        print("Usage: python garden_fencing.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]

        total_price = calculate_total_fence_price(grid)

        print(f"The total price of fencing all regions is: {total_price}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
