from typing import List, Tuple, Union

from dijkstar import Graph, find_path

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


def extract_letter(coordinates: List[Coord], x: int, y: int) -> Union[str, None]:
    return next((coordinate[2] for coordinate in coordinates if coordinate[0] == x and coordinate[1] == y), None)


def in_bounds(grid: Grid, x: int, y: int) -> bool:
    return 0 < x < len(grid[0]) and 0 < y < len(grid)


def find_connections_start(grid: Grid, coordinates: List[Coord]) -> List[Tuple[str, int]]:
    def find_connection(initial_letter: str, steps, x, y, visited) -> List[Tuple[str, int]]:
        if not in_bounds(grid, x, y):
            return []
        if grid[y][x] == "#" or grid[y][x] == " ":
            return []
        if (x, y) in visited:
            return []

        if grid[y][x].isalpha():
            # print(f'Found: {grid[y][x]}, x: {x}, y: {y}')
            letter = extract_letter(coordinates, x, y)
            if letter is not None and initial_letter != letter:
                return [f'{initial_letter}-{letter}', steps-1]  # exclude the letter itself as we count only steps

        visited.append((x, y))

        res1 = find_connection(initial_letter, steps+1, x+1, y, visited[:])
        res2 = find_connection(initial_letter, steps+1, x-1, y, visited[:])
        res3 = find_connection(initial_letter, steps+1, x, y-1, visited[:])
        res4 = find_connection(initial_letter, steps+1, x, y+1, visited[:])
        results = [res for res in [res1, res2, res3, res4] if len(res) > 0]

        return [res for res1 in results for res in res1]

    connections = []

    # res_x = find_connection('AA', 0, 9, 1, [])
    # connections.append(res_x)

    for coordinate in coordinates:
        coord_x, coord_y, letter = coordinate
        connections += find_connection(letter, 0, coord_x, coord_y, [])

    # use zip command to make letter and step pairs for now :D
    results = []
    for i, (letter_pair, steps) in enumerate(zip(connections, connections[1:])):
        if i % 2 == 0:
            results.append((letter_pair, steps))
    return results


def find_best_path(connections: List[Tuple[str, int]]):
    graph = Graph()
    for letter_pair, steps in connections:
        [left, right] = letter_pair.split("-")
        graph.add_edge(left, right, steps)
    return find_path(graph, 'AA', 'ZZ')


if __name__ == "__main__":
    grid = collect_input(file_name="input.txt")
    fix_grid(grid)
    print_grid(grid)
    letter_coordinates = find_all_letters(grid)
    print(letter_coordinates)

    connections = find_connections_start(grid, letter_coordinates)
    print(connections)

    path = find_best_path(connections)
    print(path.total_cost - 1)
