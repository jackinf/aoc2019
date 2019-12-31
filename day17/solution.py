from typing import List, Tuple

from shared.Intcode import Intcode
Grid = List[List[str]]


def collect_input(file_name):
    with open(file_name, 'r') as f:
        return [int(x) for x in f.readline().split(',')]


def read_ascii_output(registry: List[int]) -> str:
    intcode = Intcode(registry, [])
    ascii_output = ""
    for output in intcode.run():
        ascii_output += chr(output)
    return ascii_output


def ascii_into_grid(ascii_output: str) -> Grid:
    grid = []
    for line in ascii_output.split('\n'):
        if line.strip() == "":
            continue
        grid.append([x for x in line])
    return grid


def find_intersections(grid: Grid) -> List[Tuple[int, int]]:
    intersections = []
    row_count = len(grid)
    col_count = len(grid[0])
    print(f'row_count: {row_count}, col_count: {col_count}')
    for row in range(1, row_count-1):
        for col in range(1, col_count-1):
            print(f'row: {row} col: {col}')
            if grid[row][col-1] == grid[row][col+1] == grid[row-1][col] == grid[row+1][col] == grid[row][col] == "#":
                grid[row][col] = "#"
                intersections.append((row, col))
    return intersections


def get_alignment_param_sum(intersections: List[Tuple[int, int]]):
    res = 0
    for x, y in intersections:
        res += x*y
    return res


def read_test_case(file_name):
    with open(file_name, 'r') as f:
        return f.read()


if __name__ == "__main__":
    registry = collect_input("test-case-2.txt")
    ascii_output = read_ascii_output(registry)
    # ascii_output = read_test_case('test-case.txt')
    # print(ascii_output)

    grid = ascii_into_grid(ascii_output)
    # print(grid)

    intersections = find_intersections(grid)
    # print(intersections)

    total_sum = get_alignment_param_sum(intersections)
    print("PART 1")
    print(total_sum)
