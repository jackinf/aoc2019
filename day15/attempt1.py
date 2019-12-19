from typing import List, Tuple, Union
import pygame
from shared.Intcode import Intcode


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WINDOW_SIZE = [600, 600]
MARGIN = 5
WIDTH = 20
HEIGHT = 20
offset = 10

SYMBOL_PLAYER = "D"
SYMBOL_WALL = "#"

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Day 15")


with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]


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
        grid[y][x] = "E"
        print('Found exit')
        return x, y


def get_input() -> int:
    val: Union[str, None] = None
    while val is None or len(val) == 0:
        val = input("Move north (1), south (2), west (3), or east (4)\n")
        if val not in ['1', '2', '3', '4']:
            val = None
    return int(val)


def new_grid() -> Tuple[List[List[str]], int, int]:
    size = 100
    x = size//2
    y = size//2
    grid_val = [[' ' for _ in range(size)] for _ in range(size)]
    grid_val[y][x] = "D"
    return grid_val, x, y


def text_program(last_input):
    intcode = Intcode(registry, [last_input])
    grid, x, y = new_grid()
    for output in intcode.run():
        x, y = into_grid(last_input, output, x, y, grid)
        print_grid(grid, x, y)
        val = get_input()
        intcode.inputs.append(val)
        last_input = val


def get_rect_color(grid_arg: List[List[str]], x_arg: int, y_arg: int) -> Tuple[int, int, int]:
    cell_value = grid_arg[y_arg][x_arg]
    if cell_value == " ":
        return BLACK
    if cell_value == "D":
        return GREEN
    if cell_value == "#":
        return BLUE
    if cell_value == ".":
        return GRAY
    if cell_value == "E":
        return RED
    return WHITE


def gui_program():
    done = False
    clock = pygame.time.Clock()
    intcode = Intcode(registry, [], break_on_output=True)
    grid, x, y = new_grid()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                done = True

            pressed = pygame.key.get_pressed()
            input_val = -1
            if pressed[pygame.K_UP]:
                print('pressing up')
                input_val = 1
            elif pressed[pygame.K_DOWN]:
                print('pressing down')
                input_val = 2
            elif pressed[pygame.K_LEFT]:
                print('pressing left')
                input_val = 3
            elif pressed[pygame.K_RIGHT]:
                print('pressing right')
                input_val = 4

            if input_val in [1, 2, 3, 4]:
                intcode.append_input(input_val)
                output = list(intcode.run())[0]
                print(output)
                x, y = into_grid(input_val, output, x, y, grid)

            screen.fill(BLACK)

            col_max, col_min = y + offset, y - offset
            row_max, row_min = x + offset, x - offset
            for column in range(col_min, col_max):
                for row in range(row_min, row_max):
                    yy = (MARGIN + WIDTH) * (column-col_min) + MARGIN
                    xx = (MARGIN + HEIGHT) * (row-row_min) + MARGIN
                    rect_color = get_rect_color(grid, row, column)
                    # print(f'xx: {xx}, yy: {yy}, row: {row}, column: {column}, rect_color: {rect_color}')
                    pygame.draw.rect(screen, rect_color, pygame.Rect(xx, yy, WIDTH, HEIGHT))
            # print("====")

            clock.tick(30)
            pygame.display.flip()

    pygame.quit()


gui_program()