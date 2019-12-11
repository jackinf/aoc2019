from typing import Union, Tuple

from day10.asteroid import Asteroid
from day10.grid import Grid


class AsteroidManager:
    def build_grid(self, input_str: str) -> Grid:
        lines = input_str.split('\n')
        rows_count = len(lines)
        cols_count = len(lines[0])
        grid = Grid([[None for _ in range(rows_count)] for _ in range(cols_count)])

        for y in range(cols_count):
            for x in range(rows_count):
                if lines[y][x] == "#":
                    grid.create_new_at(x, y)

        return grid

    def find_asteroids_for_all(self, grid: Grid):
        for line in grid.cols:
            for item in line:
                if item is not None:
                    self.find_asteroids_for_current(grid, item)

    def find_asteroids_for_current(self, grid: Grid, current: Asteroid):
        rows_count, cols_count = grid.get_rows_cols_count()

        left_vertical = [(current.x-1, i) for i in range(rows_count)]
        right_vertical = [(current.x+1, i) for i in range(rows_count)]
        upper_horizontal = [(i, current.y-1) for i in range(cols_count)]
        lower_horizontal = [(i, current.y+1) for i in range(cols_count)]

        combined = left_vertical + right_vertical + upper_horizontal + lower_horizontal
        current.blocked_asteroids.append([current.x, current.y])

        for start_x, start_y in combined:
            delta_x, delta_y = start_x - current.x, start_y - current.y
            x, y = current.x + delta_x, current.y + delta_y
            found = False
            while 0 <= x < cols_count and 0 <= y < rows_count:
                if grid.has_asteroid_at(x, y) and not current.is_blocked(x, y):
                    if found:
                        current.blocked_asteroids.append([x, y])
                    else:
                        current.seen_asteroids.append([x, y])
                        current.blocked_asteroids.append([x, y])
                        found = True
                x, y = x + delta_x, y + delta_y

        for asteroid in grid.get_all_asteroids():
            if not current.is_blocked(asteroid.x, asteroid.y) and \
                    not current.has_seen(asteroid.x, asteroid.y) and \
                    not current.is_same(asteroid):
                current.seen_asteroids.append([asteroid.x, asteroid.y])

        pass

    def ask_all_asteroids_how_much_they_see(self, grid: Grid) -> Tuple[Union[None, Asteroid], int]:
        max_asteroids_seen = 0
        max_asteroid: Union[None, Asteroid] = None
        for line in grid.cols:
            for item in line:
                if item is not None:
                    print(item.get_how_much_asteroids_i_see())
                    if max_asteroids_seen < len(item.seen_asteroids):
                        max_asteroids_seen = len(item.seen_asteroids)
                        max_asteroid = item
        return max_asteroid, max_asteroids_seen

test_case_0 = """....#
.....
..##.
.#...
#...."""

test_case_1 = """.#..#
.....
#####
....#
...##"""

# Best is 5,8 with 33 other asteroids detected:
test_case_2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

manager = AsteroidManager()

grid1 = manager.build_grid(test_case_2)
manager.find_asteroids_for_all(grid1)
max_asteroid, seen = manager.ask_all_asteroids_how_much_they_see(grid1)
print(max_asteroid, seen)

# with open('input.txt', 'r') as f:
#     entire_line = ''.join(f.readlines())
#     grid2 = manager.build_grid(entire_line)
#     manager.find_asteroids_for_all(grid2)
#     max_asteroid, max_asteroids_seen = manager.ask_all_asteroids_how_much_they_see(grid2)
#     print(max_asteroids_seen)
