import sys
from collections import deque

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

def compute_perimeter(grid, region):
    """
    Compute the perimeter for a region:
    For each cell in the region, count edges that are exposed 
    (either out of bounds or adjacent to a different character).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    region_cells = set(region['cells'])
    char = region['char']
    perimeter = 0
    for (r,c) in region['cells']:
        # Check each of the 4 directions
        for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != char:
                perimeter += 1
    return perimeter

def calculate_total_fence_price(grid):
    """
    Calculate the total fence price for all regions in the grid.
    Price = sum(area(region) * perimeter(region)) for all regions.
    """
    regions = find_regions(grid)
    total_price = 0
    for region in regions:
        area = len(region['cells'])
        perimeter = compute_perimeter(grid, region)
        total_price += area * perimeter
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
