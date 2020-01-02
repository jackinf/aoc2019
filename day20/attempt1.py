from typing import List, Tuple

Grid = List[List[str]]
Coord = Tuple[int, int, str]


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


def get_letter_coordinate(grid: Grid, x: int, y: int) -> Coord:
    # Vertical conditions
    if grid[y+1][x] == "." and grid[y-1][x].isalpha():
        return x, y, grid[y-1][x] + grid[y][x]
    if grid[y-1][x] == "." and grid[y+1][x].isalpha():
        return x, y, grid[y][x] + grid[y+1][x]

    # Horizontal conditions
    if grid[y][x+1] == "." and grid[y][x-1].isalpha():
        return x, y, grid[y][x-1] + grid[y][x]
    if grid[y][x-1] == "." and grid[y][x+1].isalpha():
        return x, y, grid[y][x] + grid[y][x+1]

    return None


def find_all_letters(grid: Grid):
    found = []
    for y in range(1, len(grid)-1):
        for x in range(1, len(grid[0])-1):
            if grid[y][x].isalpha():
                item = get_letter_coordinate(grid, x, y)
                if item is not None:
                    found.append(item)
    return found


def find_connections_start(grid: Grid, coordinates: List[Coord]) -> List[Tuple[str, int]]:
    def find_connection(steps, x, y, visited) -> List[Tuple[str, int]]:
        if 0 > x or len(grid[0]) <= x or 0 > y or len(grid) <= y or grid[y][x] == "#":
            return []

        if grid[y][x].isalpha():
            letter = next((coordinate[2] for coordinate in coordinates if coordinate[0] == x and coordinate[1] == y), None)
            if letter is None:
                raise Exception(f"letter not found at x:{x}, y:{y}")
            return [letter, steps]

        visited.append((x, y))

        results = []
        results += find_connection(steps+1, x+1, y, visited[:])
        results += find_connection(steps+1, x-1, y, visited[:])
        results += find_connection(steps+1, x, y-1, visited[:])
        results += find_connection(steps+1, x, y+1, visited[:])
        results = [res for res in results if len(res) > 0]

        return results

    connections = []
    for coordinate in coordinates:
        coord_x, coord_y, letter = coordinate
        connections += find_connection(0, coord_x, coord_y, [])
    return connections


if __name__ == "__main__":
    grid = collect_input(file_name="test-case-1.txt")
    fix_grid(grid)
    print_grid(grid)
    letter_coordinates = find_all_letters(grid)
    print(letter_coordinates)

    connections = find_connections_start(grid, letter_coordinates)
    print(connections)


