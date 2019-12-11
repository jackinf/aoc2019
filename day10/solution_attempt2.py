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
        for asteroid in grid.get_all_asteroids():
            current.add_other_asteroid(asteroid)
        current.clean_up_blocked()

    def ask_all_asteroids_how_much_they_see(self, grid: Grid) -> Tuple[Union[None, Asteroid], int]:
        max_asteroids_seen = 0
        max_asteroid: Union[None, Asteroid] = None
        for asteroid in grid.get_all_asteroids():
            # print(asteroid.get_how_much_other_asteroids_i_see())
            if max_asteroids_seen < len(asteroid.other_asteroids):
                max_asteroids_seen = len(asteroid.other_asteroids)
                max_asteroid = asteroid
        return max_asteroid, max_asteroids_seen


am = AsteroidManager()

with open('input.txt', 'r') as f:
    matrix1 = am.build_matrix('\n' + ''.join(f.readlines()))
    grid1 = am.build_grid(matrix1)
    # grid1.print_grid()

    print("PART 1")
    am.find_asteroids_for_all(grid1)
    print(am.ask_all_asteroids_how_much_they_see(grid1))

