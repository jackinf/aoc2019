import math
from typing import List, Tuple

Grid = List[List[str]]


def collect_input(file_name: str) -> Grid:
    with open(file_name, 'r') as f:
        return [[x for x in line] for line in f.read().splitlines()]


def calculate_biodiversity(grid: Grid) -> int:
    flat = [x for y in grid for x in y]
    sum = 0
    for i in range(len(flat)):
        if flat[i] == "#":
            sum += math.pow(2, i)
    return int(sum)


def count_adjacent_bugs(grid: Grid, x: int, y: int):
    how_many = 0
    if len(grid[y]) > x+1 and grid[y][x+1] == "#":
        how_many += 1
    if x-1 >= 0 and grid[y][x-1] == "#":
        how_many += 1
    if len(grid) > y+1 and grid[y+1][x] == "#":
        how_many += 1
    if y-1 >= 0 and grid[y-1][x] == "#":
        how_many += 1
    return how_many


def step(grid: Grid):
    to_change: List[Tuple[int, int, str]] = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            adjacent_bug_count = count_adjacent_bugs(grid, x, y)
            if grid[y][x] == "#" and adjacent_bug_count != 1:
                to_change.append((x, y, '.'))
            elif grid[y][x] == "." and adjacent_bug_count in [1, 2]:
                to_change.append((x, y, '#'))
    for x, y, letter in to_change:
        grid[y][x] = letter


def print_grid(grid: Grid):
    res = ""
    for line in grid:
        res += "".join(line) + "\n"
    print(res)


if __name__ == "__main__":
    grid = collect_input("input.txt")
    print_grid(grid)

    biodiversities = []

    while True:
        bio = calculate_biodiversity(grid)
        if bio in biodiversities:
            print(f'Part 1: {bio}')
            break
        biodiversities.append(bio)

        step(grid)
