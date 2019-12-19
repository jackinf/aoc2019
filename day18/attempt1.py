import copy
from typing import List
import numpy as np
Grid = List[List[str]]


def collect_input(file_name) -> Grid:
    with open(file_name, 'r') as f:
        return [[x for x in line if x != "\n"] for line in f.readlines()]


def get_letter_locations(grid: Grid):
    arr = np.array(grid)
    letters = [x for x in arr.flatten() if x not in [".", "#"]]
    upper_letters = [x for x in letters if x.isupper()]
    lower_letters = [x for x in letters if not x.isupper()]
    return upper_letters, lower_letters


def simplity_grid(grid: Grid) -> Grid:
    new_grid = copy.deepcopy(grid)
    for row in range(len(grid)-1):
        for col in range(len(grid[0])-1):
            if grid[row][col] == " ":
                if grid[row][col-1] == grid[row][col+1] == grid[row+1][col] == "#" \
                    or grid[row][col-1] == grid[row][col+1] == grid[row-1][col] == "#" \
                    or grid[row-1][col] == grid[row+1][col] == grid[row][col+1] == "#" \
                    or grid[row-1][col] == grid[row+1][col] == grid[row][col-1] == "#":
                    new_grid[row][col] = "#"
    return new_grid

if __name__ == "__main__":
    grid = collect_input("test-case-1.txt")
    print(grid)