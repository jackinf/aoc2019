from typing import List

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
    pass


if __name__ == "__main__":
    registry = collect_input("input.txt")
    intcode = Intcode(registry, [0, 0], break_on_output=True)
    output = next(intcode.run())
    print(output)

    grid = create_grid(10, 10)
    draw_grid(grid)

