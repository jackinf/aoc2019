from typing import List, Tuple, Union

from day10.asteroid import Asteroid
from day10.grid import Grid

Matrix = List[List[str]]


class AsteroidManager:
    def build_matrix(self, test_case: str) -> Matrix:
        matrix = []
        for letter in test_case:
            if letter == '\n':
                matrix.append([])
                continue
            matrix[-1].append(letter)
        return matrix

    def build_grid(self, matrix: Matrix) -> Grid:
        rows = len(matrix)
        cols = len(matrix[0])
        grid = Grid([[None for _ in range(cols)] for _ in range(rows)])
        for y in range(cols):
            for x in range(rows):
                if matrix[y][x] == "#":
                    grid.create_new_at(x, y)
        return grid

    def find_asteroids_for_all(self, grid: Grid):
        for asteroid in grid.get_all_asteroids():
            self.find_asteroids_for_current(grid, asteroid)

    def find_asteroids_for_current(self, grid: Grid, current: Asteroid):
        rows_count, cols_count = grid.get_rows_cols_count()
        current.seen_asteroids.clear()
        current.blocked_asteroids.clear()

        left_vertical = [(current.x-1, i) for i in range(rows_count)]
        right_vertical = [(current.x+1, i) for i in range(rows_count)]
        upper_horizontal = [(i, current.y-1) for i in range(cols_count)]
        lower_horizontal = [(i, current.y+1) for i in range(cols_count)]

        combined = left_vertical + right_vertical + upper_horizontal + lower_horizontal

        # find all blocked asteroids
        for start_x, start_y in combined:
            delta_x, delta_y = start_x - current.x, start_y - current.y
            x, y = current.x + delta_x, current.y + delta_y
            found = False
            while 0 <= x < cols_count and 0 <= y < rows_count:
                if grid.has_asteroid_at(x, y) and not current.is_blocked(x, y):
                    if found:
                        current.blocked_asteroids.append(grid.get(x, y))
                    else:
                        found = True
                x, y = x + delta_x, y + delta_y

        # find all rest asteroids which are not blocked
        for asteroid in grid.get_all_asteroids():
            if not current.is_blocked(asteroid.x, asteroid.y) and \
                    not current.has_seen(asteroid.x, asteroid.y) and \
                    not current.is_same(asteroid):
                current.seen_asteroids.append([asteroid.x, asteroid.y])

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


case_1 = """
.#.
...
###"""

# (3, 4) has 8 asteroids
case_2 = """
.#..#
.....
#####
....#
...##"""

# Best is 5,8 with 33 other asteroids detected:
case_3 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

case_4 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

case_5 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

case_6 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

am = AsteroidManager()
matrix1 = am.build_matrix(case_3)
# print(matrix1)
grid1 = am.build_grid(matrix1)
grid1.print_grid()

asteroid12 = grid1.get(0, 8)
print(asteroid12)
am.find_asteroids_for_current(grid1, asteroid12)
print(asteroid12.blocked_asteroids)
print(asteroid12.seen_asteroids)

am.find_asteroids_for_all(grid1)
print(am.ask_all_asteroids_how_much_they_see(grid1))


