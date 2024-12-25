#!/usr/bin/env python3
import sys

def parse_grid(lines):
    """
    Convert 7 lines (each 5 chars) into a 7x5 array of 0/1.
    '#' => 1
    '.' => 0
    """
    if len(lines) != 7 or any(len(line) != 5 for line in lines):
        raise ValueError("Each schematic must be exactly 7 lines of 5 characters.")
    grid = []
    for row in lines:
        grid.append([1 if ch == '#' else 0 for ch in row])
    return grid

def is_lock(lines):
    """
    Identify a 'lock' schematic based on puzzle convention:
    - Top row is '#####'
    - Bottom row is '.....'
    """
    return lines[0] == "#####" and lines[-1] == "....."

def is_key(lines):
    """
    Identify a 'key' schematic based on puzzle convention:
    - Top row is '.....'
    - Bottom row is '#####'
    """
    return lines[0] == "....." and lines[-1] == "#####"

def grids_fit(lock_grid, key_grid):
    """
    Return True if for every (row, col), we do NOT have a collision:
      lock_grid[row][col] == 1 and key_grid[row][col] == 1
    """
    for row in range(7):
        for col in range(5):
            if lock_grid[row][col] == 1 and key_grid[row][col] == 1:
                return False
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python day25.py <input.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Read file lines, strip whitespace, ignore empty lines
    with open(filename, 'r') as f:
        raw = [line.strip() for line in f if line.strip()]
    
    # Must be multiple of 7 lines to form schematics
    if len(raw) % 7 != 0:
        raise ValueError(f"File {filename} does not contain a multiple of 7 lines (after removing blanks).")
    
    locks = []
    keys = []
    
    # Parse each block of 7 lines as a single schematic
    for i in range(0, len(raw), 7):
        block = raw[i : i+7]
        if is_lock(block):
            locks.append(parse_grid(block))
        elif is_key(block):
            keys.append(parse_grid(block))
        else:
            # Not recognized as lock or key => raise or skip
            raise ValueError("Schematic doesn't match known lock/key format:\n" + "\n".join(block))
    
    # Try all lock–key combinations
    fit_count = 0
    for lock_grid in locks:
        for key_grid in keys:
            if grids_fit(lock_grid, key_grid):
                fit_count += 1
    
    print(f"Number of fitting lock–key pairs: {fit_count}")

if __name__ == "__main__":
    main()
