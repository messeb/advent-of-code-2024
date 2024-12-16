import sys
import heapq

def parse_maze(filename):
    with open(filename, 'r') as f:
        maze = [list(line.rstrip('\n')) for line in f]
    return maze

def find_positions(maze):
    start = None
    end = None
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == 'S':
                start = (r, c)
            elif ch == 'E':
                end = (r, c)
    return start, end

def in_bounds(r, c, maze):
    return 0 <= r < len(maze) and 0 <= c < len(maze[0])

def is_wall(r, c, maze):
    return maze[r][c] == '#'

def main():
    if len(sys.argv) != 2:
        print("Usage: python reindeer_maze.py input.txt")
        sys.exit(1)

    filename = sys.argv[1]
    maze = parse_maze(filename)
    start, end = find_positions(maze)
    if start is None or end is None:
        print("Error: Start or End not found in the maze.")
        sys.exit(1)

    # Directions: 0=North,1=East,2=South,3=West
    # Start facing East (direction=1)
    start_state = (start[0], start[1], 1)
    
    moves = [(-1,0),(0,1),(1,0),(0,-1)]
    # Dijkstra for part one
    dist = {}
    dist[start_state] = 0
    pq = []
    heapq.heappush(pq, (0, start_state))

    end_min_dist = None
    end_states = []

    while pq:
        cost, (r,c,d) = heapq.heappop(pq)
        if dist[(r,c,d)] < cost:
            continue
        if (r,c) == end:
            if end_min_dist is None or cost < end_min_dist:
                end_min_dist = cost
                end_states = [(r,c,d)]
            elif cost == end_min_dist:
                end_states.append((r,c,d))
            continue

        # forward
        nr, nc = r+moves[d][0], c+moves[d][1]
        if in_bounds(nr, nc, maze) and not is_wall(nr, nc, maze):
            new_cost = cost + 1
            new_state = (nr, nc, d)
            if new_state not in dist or new_cost < dist[new_state]:
                dist[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))

        # turn left
        left_d = (d-1)%4
        left_cost = cost + 1000
        left_state = (r,c,left_d)
        if left_state not in dist or left_cost < dist[left_state]:
            dist[left_state] = left_cost
            heapq.heappush(pq, (left_cost, left_state))

        # turn right
        right_d = (d+1)%4
        right_cost = cost + 1000
        right_state = (r,c,right_d)
        if right_state not in dist or right_cost < dist[right_state]:
            dist[right_state] = right_cost
            heapq.heappush(pq, (right_cost, right_state))

    if end_min_dist is None:
        print("No path found.")
        return

    # Print minimal score
    print(f"The minimal score is: {end_min_dist}")

    # Part two: find all tiles on minimal paths
    stack = []
    visited_states = set()
    for es in end_states:
        stack.append(es)
        visited_states.add(es)

    on_path_tiles = set()

    while stack:
        r,c,d = stack.pop()
        on_path_tiles.add((r,c))
        cost = dist[(r,c,d)]

        # Check forward predecessor
        # If forward: prev_state=(r-dr,c-dc,d) with dist[prev]+1=cost
        rr, cc = r - moves[d][0], c - moves[d][1]
        if in_bounds(rr, cc, maze) and not is_wall(rr, cc, maze):
            prev_state = (rr, cc, d)
            if prev_state in dist:
                if dist[prev_state] + 1 == cost:
                    if prev_state not in visited_states:
                        visited_states.add(prev_state)
                        stack.append(prev_state)

        # Check turn left predecessor
        prev_d_left = (d+1)%4
        prev_state_left = (r,c,prev_d_left)
        if prev_state_left in dist:
            if dist[prev_state_left] + 1000 == cost:
                if prev_state_left not in visited_states:
                    visited_states.add(prev_state_left)
                    stack.append(prev_state_left)

        # Check turn right predecessor
        prev_d_right = (d-1)%4
        prev_state_right = (r,c,prev_d_right)
        if prev_state_right in dist:
            if dist[prev_state_right] + 1000 == cost:
                if prev_state_right not in visited_states:
                    visited_states.add(prev_state_right)
                    stack.append(prev_state_right)

    count = 0
    for (rr,cc) in on_path_tiles:
        if maze[rr][cc] != '#':
            count += 1

    # Print tiles count
    print(f"The number of tiles on best paths is: {count}")

if __name__ == "__main__":
    main()
