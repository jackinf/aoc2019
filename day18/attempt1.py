import copy
from time import sleep
from typing import List, Union, Tuple
import numpy as np

Grid = List[List[str]]
PLAYER_CHAR = "@"
FLOOR_CHAR = "."
WALL_CHAR = "#"
CoordAndLetter = Tuple[int, int, str]
DoorInfo = Tuple[int, int, str]


def print_grid(grid: Grid):
    res = ""
    for line in grid:
        res += "".join([item for item in line]) + "\n"
    print(res + "\n")


def collect_input(file_name) -> Grid:
    with open(file_name, 'r') as f:
        return [[x for x in line if x != "\n"] for line in f.readlines()]


def get_all_letter_with_coordinates(grid: Grid) -> List[CoordAndLetter]:
    arr = np.array(grid)

    # mark all excluded values with x and filter x out. TODO: find a better way
    arr = np.where(arr == ".", "x", arr)
    arr = np.where(arr == "#", "x", arr)
    arr = np.where(arr == "@", "x", arr)
    res = np.where(arr != "x")

    coordiates = list(zip(res[0], res[1]))
    return [(x, y, grid[x][y]) for x, y in coordiates]


def get_keys(coordinates: List[CoordAndLetter]) -> List[CoordAndLetter]:
    return [coord for coord in coordinates if coord[2].islower()]

def get_doors(coordinates: List[CoordAndLetter]) -> List[CoordAndLetter]:
    return [coord for coord in coordinates if coord[2].isupper()]


def unlock_door(grid: Grid, letter: str):
    coordinates = get_all_letter_with_coordinates(grid)
    the_key = next((key for key in get_keys(coordinates) if key[2] == letter))
    the_door = next((door for door in get_doors(coordinates) if door[2] == letter.upper()), None)
    p_x, p_y = find_player_pos(grid)
    grid[p_x][p_y] = "."
    grid[the_key[0]][the_key[1]] = PLAYER_CHAR
    if the_door is not None:
        grid[the_door[0]][the_door[1]] = FLOOR_CHAR


def simplity_grid(grid: Grid) -> Grid:
    new_grid = copy.deepcopy(grid)
    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid[0]) - 1):
            if grid[row][col] != "#":
                if grid[row][col - 1] == grid[row][col + 1] == grid[row + 1][col] == "#" \
                        or grid[row][col - 1] == grid[row][col + 1] == grid[row - 1][col] == "#" \
                        or grid[row - 1][col] == grid[row + 1][col] == grid[row][col + 1] == "#" \
                        or grid[row - 1][col] == grid[row + 1][col] == grid[row][col - 1] == "#":
                    new_grid[row][col] = "#"
    return new_grid


def find_player_pos(grid: Grid) -> Tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                return i, j
    raise Exception("Player not found")


def to_visited_index(x: int, y: int) -> int:
    return x * 100000 + y


def get_distance_to_letter(grid: Grid, x: int, y: int, letter: str, distance: int, visited: [int]) -> Union[int, None]:
    if grid[x][y] == "#" or grid[x][y].isupper() or to_visited_index(x, y) in visited:
        return None
    if grid[x][y] == letter:
        return distance

    visited.append(to_visited_index(x, y))

    # small optimization: copy visited cells only if we are at intersection
    # we need to clone the values so that 2+ different paths won't intersect with each other
    def is_intersection():
        cells = [grid[x-1][y], grid[x+1][y], grid[x][y-1], grid[x][y+1]]
        return len([cell for cell in cells if cell == "#"]) <= 2  # there are at most 2 walls near the cell
    visited = visited[:] if is_intersection() else visited

    res1 = get_distance_to_letter(grid, x-1, y, letter, distance+1, visited)
    res2 = get_distance_to_letter(grid, x+1, y, letter, distance+1, visited)
    res3 = get_distance_to_letter(grid, x, y-1, letter, distance+1, visited)
    res4 = get_distance_to_letter(grid, x, y+1, letter, distance+1, visited)

    results = [res for res in [res1, res2, res3, res4] if res is not None]
    if len(results) > 0:
        return min(results)
    return None


def start_find_maze_paths(grid: Grid):
    keys_len = len(get_keys(get_all_letter_with_coordinates(grid)))
    found_distances = find_maze_paths(grid, 0, '', keys_len, None)
    full_path_found_distances = [found_distance for found_distance in found_distances if len(found_distance[0]) == keys_len]
    full_path_shortest_distance = min(full_path_found_distances, key= lambda t: t[1])
    print(full_path_shortest_distance)


def find_maze_paths(grid: Grid, total_distance: int, path: str, keys_len, keyarg: Union[str, None]) -> List[Tuple[str, int]]:
    grid = copy.deepcopy(grid)
    if keyarg is not None:
        unlock_door(grid, keyarg)
    # print(f'Path: {path}, Total distance: {total_distance}')
    # print_grid(grid)
    # sleep(1)

    keys = get_keys(get_all_letter_with_coordinates(grid))
    if len(keys) == 0 and len(path) == keys_len:
        print(f'Path: {path}, Total distance: {total_distance}')
        return [(path, total_distance)]

    distances = []
    for key in keys:
        key_letter = key[2]
        player_x, player_y = find_player_pos(grid)
        b_dist = get_distance_to_letter(grid, player_x, player_y, key_letter, 0, [])
        if b_dist is None:
            continue

        results = find_maze_paths(grid, total_distance + b_dist, path + key_letter, keys_len, key[2])
        distances += results

    return distances


def run_test(grid: Grid):
    print_grid(grid)
    player_x, player_y = find_player_pos(grid)
    b_dist = get_distance_to_letter(copy.deepcopy(grid), player_x, player_y, 'a', 0, [])
    unlock_door(grid, 'a')
    print_grid(grid)
    print(b_dist)


if __name__ == "__main__":
    grid = collect_input("test-case-1.txt")
    print_grid(grid)
    start_find_maze_paths(grid)
