import copy
import sys
from typing import List, Union, Tuple
import numpy as np

Grid = List[List[str]]


def print_grid(grid: Grid):
    res = ""
    for line in grid:
        res += "".join([item for item in line]) + "\n"
    print(res + "\n")


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
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            if grid[row][col] != "#":
                if grid[row][col - 1] == grid[row][col + 1] == grid[row + 1][col] == "#" \
                        or grid[row][col - 1] == grid[row][col + 1] == grid[row - 1][col] == "#" \
                        or grid[row - 1][col] == grid[row + 1][col] == grid[row][col + 1] == "#" \
                        or grid[row - 1][col] == grid[row + 1][col] == grid[row][col - 1] == "#":
                    new_grid[row][col] = "#"
    return new_grid


def find_player_pos(grid: Grid) -> Tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                return i, j
    raise Exception("Player not found")


def to_visited_index(x: int, y: int) -> int:
    return x * 100000 + y


def get_distance_to_letter(grid: Grid, x: int, y: int, letter: str, distance: int, visited: [int]) -> Union[int, None]:
    if grid[x][y] == "#" or grid[x][y].isupper() or to_visited_index(x, y) in visited:
        return None
    if grid[x][y] == letter:
        return distance

    visited.append(to_visited_index(x, y))
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            res1 = get_distance_to_letter(grid, x-1, y, letter, distance+1, visited)
            res2 = get_distance_to_letter(grid, x+1, y, letter, distance+1, visited)
            res3 = get_distance_to_letter(grid, x, y-1, letter, distance+1, visited)
            res4 = get_distance_to_letter(grid, x, y+1, letter, distance+1, visited)

            results = [res for res in [res1, res2, res3, res4] if res is not None]
            if len(results) > 0:
                return min(results)
    return None

if __name__ == "__main__":
    grid = collect_input("test-case-0.txt")
    print_grid(grid)
    print(get_letter_locations(grid))
    print_grid(grid)

    player_x, player_y = find_player_pos(grid)
    b_dist = get_distance_to_letter(copy.deepcopy(grid), player_x, player_y, 'x', 0, [])
    print(b_dist)