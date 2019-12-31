import math
from typing import List, Generator

from shared.Intcode import Intcode
Grid = List[List[str]]


def collect_input(file_name: str) -> List[int]:
    with open(file_name, 'r') as f:
        return [int(x) for x in f.readline().split(',')]


def create_grid(rows: int, cols: int) -> Grid:
    return [['.' for _ in range(cols)] for _ in range(rows)]


def draw_grid(grid: Grid):
    res = ""
    for line in grid:
        res += "".join(line) + "\n"
    print(res)


def draw_tractor_beam(grid: Grid):
    a_upper = math.tan(math.radians(50))
    a_lower = math.tan(math.radians(30))
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            lower = x * a_lower
            upper = x * a_upper
            if lower <= y <= upper:
                grid[y][x] = "#"


def count_beam_points(grid: Grid):
    return len([item for subarray in grid for item in subarray if item == "#"])


if __name__ == "__main__":
    registry = collect_input("test-case-2.txt")

    result = 0
    for i in range(50):
        for j in range(50):
            intcode = Intcode(registry, [i, j], break_on_output=True)
            output = next(intcode.run())
            if output == 1:
                result += 1
                print(f'x: {i}, y: {j}')
    print(f'Part 1: {result}')

    grid = create_grid(10, 10)
    draw_tractor_beam(grid)
    draw_grid(grid)
    print(count_beam_points(grid))

