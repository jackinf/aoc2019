from typing import List, Tuple

from shared.Intcode import Intcode

with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]


def print_grid(grid_val: List[List[str]]):
    for y in range(len(grid_val)):
        print(grid_val[y])


def into_grid(input_val: int, output_val: int, x: int, y: int, grid: List[List[str]]) -> Tuple[int, int]:
    if output_val == 1 or output_val == 0:
        grid[y][x] = "."

        if output_val == 0:
            grid[y][x] = "D"
            if input_val == 1:
                grid[y-1][x] = "#"
            if input_val == 2:
                grid[y+1][x] = "#"
            if input_val == 3:
                grid[y][x-1] = "#"
            if input_val == 4:
                grid[y][x+1] = "#"

        if output_val == 1:
            if input_val == 1:
                y -= 1
            if input_val == 2:
                y += 1
            if input_val == 3:
                x -= 1
            if input_val == 4:
                x += 1
            grid[y][x] = "D"

        return x, y
    else:
        print('Found exit')
        return x, y


last_input = 1
intcode = Intcode(registry, [last_input])
x = 5
y = 5
grid = [[' ' for _ in range(10)] for _ in range(10)]
for output in intcode.run():
    x, y = into_grid(last_input, output, x, y, grid)
    print_grid(grid)
    val = int(input("Move north (1), south (2), west (3), or east (4)\n"))
    intcode.inputs.append(val)
    last_input = val
