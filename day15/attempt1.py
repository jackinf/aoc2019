from typing import List, Tuple, Union

from shared.Intcode import Intcode

with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]


offset = 10
def print_grid(grid_val: List[List[str]], xx: int, yy: int):
    print(f'x: {xx}, y: {yy}')
    for y in range(yy - offset, yy + offset):
        for x in range(xx - offset, xx + offset):
            print(grid_val[y][x], end = '')
        print('')


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
x = 50
y = 50
grid = [[' ' for _ in range(100)] for _ in range(100)]
for output in intcode.run():
    x, y = into_grid(last_input, output, x, y, grid)
    print_grid(grid, x, y)
    val: Union[str, None] = None
    while val is None or len(val) == 0:
        val = input("Move north (1), south (2), west (3), or east (4)\n")
        if val not in ['1', '2', '3', '4']:
            val = None
    intcode.inputs.append(int(val))
    last_input = int(val)
