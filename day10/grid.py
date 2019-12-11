from typing import List, Union, Generator, Tuple

from day10.asteroid import Asteroid


class Grid:
    def __init__(self, cols: List[List[Union[None, Asteroid]]]):
        self.cols = cols

    def get(self, x: int, y: int) -> Union[None, Asteroid]:
        return self.cols[y][x]

    def create_new_at(self, x: int, y: int):
        self.cols[y][x] = Asteroid(x, y)

    def has_asteroid_at(self, x: int, y: int) -> bool:
        return self.cols[y][x] is not None

    def get_all_asteroids(self) -> Generator[Asteroid, None, None]:
        for col in self.cols:
            for cell in col:
                if cell is not None:
                    yield cell

    def get_rows_cols_count(self) -> Tuple[int, int]:
        col_count = len(self.cols)
        row_count = len(self.cols[0])
        return row_count, col_count

    def print_grid(self):
        print('PRINTING GRID')
        print(self.cols)
        output = ""
        rows, cols = self.get_rows_cols_count()
        for y in range(cols):
            for x in range(rows):
                cell = self.cols[y][x]
                output += "#" if cell is not None else "."
            output += '\n'
        print(output)
