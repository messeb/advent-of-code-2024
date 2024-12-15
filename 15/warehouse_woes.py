import sys

def read_input(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if "\n\n" not in data:
        print("Error: Expected a blank line separating map and moves.")
        sys.exit(1)

    arr, moves = data.split("\n\n", 1)
    moves = moves.replace("\n", "")
    return arr, moves

def transform_map(arr):
    # Apply transformations for scaled scenario
    arr = arr.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
    return arr

def find_robot(grid, scaled):
    n, m = len(grid), len(grid[0])
    if scaled:
        # Robot = '@.'
        for i in range(1, n-1):
            j = 1
            while j < m-1:
                if j+1 < m and grid[i][j] == '@' and grid[i][j+1] == '.':
                    return i, j
                j += 1
    else:
        # Robot = '@'
        for i in range(1, n-1):
            for j in range(1, m-1):
                if grid[i][j] == '@':
                    return i, j
    print("Error: Robot not found.")
    sys.exit(1)

def simulate_moves(grid, moves, scaled):
    n, m = len(grid), len(grid[0])
    x, y = find_robot(grid, scaled)

    d = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    for move in moves:
        dx, dy = d[move]
        to_move = [(x, y)]
        flag = True
        for (i2, j2) in to_move:
            nx, ny = i2 + dx, j2 + dy
            if (nx, ny) not in to_move:
                if grid[nx][ny] == "#":
                    # wall
                    flag = False
                    break
                if scaled:
                    # Boxes: '[]'
                    if grid[nx][ny] == "[":
                        to_move.extend([(nx, ny), (nx, ny + 1)])
                    elif grid[nx][ny] == "]":
                        to_move.extend([(nx, ny), (nx, ny - 1)])
                else:
                    # Unscaled: 'O' for boxes
                    if grid[nx][ny] == "O":
                        to_move.append((nx, ny))

        if flag:
            for (ii, jj) in reversed(to_move):
                grid[ii + dx][jj + dy], grid[ii][jj] = grid[ii][jj], grid[ii + dx][jj + dy]
            x, y = x + dx, y + dy

    return grid

def compute_gps_sum(grid, scaled):
    n, m = len(grid), len(grid[0])
    box_char = '[' if scaled else 'O'
    total = 0
    for i in range(1, n-1):
        for j in range(1, m-1):
            if grid[i][j] == box_char:
                total += 100*i + j
    return total

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python warehouse_woes.py input.txt [--scaled]")
        sys.exit(1)

    filename = sys.argv[1]
    scaled = False
    if len(sys.argv) == 3:
        if sys.argv[2] == '--scaled':
            scaled = True
        else:
            print("Invalid argument. Use '--scaled' to enable scaling.")
            sys.exit(1)

    arr, moves = read_input(filename)
    if scaled:
        arr = transform_map(arr)

    grid = [list(line) for line in arr.split("\n")]
    # Simulate moves
    grid = simulate_moves(grid, moves, scaled)
    # Compute and print result
    result = compute_gps_sum(grid, scaled)
    print(result)

if __name__ == "__main__":
    main()
