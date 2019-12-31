from typing import List, Tuple

Grid = List[List[str]]


def collect_input(file_name: str) -> Grid:
    with open(file_name, 'r') as f:
        return [[x for x in line if x != "\n"] for line in f.readlines()]


def fix_grid(grid: Grid):
    max_len = max([len(line) for line in grid])
    for line in grid:
        diff = max_len - len(line)
        if diff > 0:
            line.extend([' '] * diff)


def print_grid(grid: Grid):
    res = ""
    for line in grid:
        res += "".join(line) + '\n'
    print(res)


def get_letter_coordinate(grid: Grid, x: int, y: int) -> Tuple[int, int, str]:
    if grid[y+1][x].isalpha():
        return x, y, grid[y][x] + grid[y+1][x]
    if  grid[y][x+1].isalpha():
        return x, y, grid[y][x] + grid[y][x+1]


def find_all_letters(grid: Grid):
    found = []
    for y in range(len(grid)-1):
        for x in range(len(grid[0])-1):
            if grid[y][x].isalpha():
                item = get_letter_coordinate(grid, x, y)
                if item not in found:
                    found.append(item)
    return found


if __name__ == "__main__":
    grid = collect_input(file_name="test-case-1.txt")
    fix_grid(grid)
    print_grid(grid)
    letter_coordinates = find_all_letters(grid)
    print(letter_coordinates)


