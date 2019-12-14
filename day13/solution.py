from enum import IntEnum
from typing import List, Dict, Tuple

from shared.Intcode import Intcode


class Tile(IntEnum):
    Empty = 0,
    Wall = 1,
    Block = 2,
    HorizontalPaddle = 3,
    Ball = 4


class CollectCellAction(IntEnum):
    GetX = 0,
    GetY = 1,
    GetTile = 2


class Cell:
    def __init__(self, x: int, y: int, tile: Tile):
        self.x = x
        self.y = y
        self.tile = tile


class Arcade:
    def __init__(self, registry: List[int]):
        registry[0] = 2
        self.intcode = Intcode(registry, [0])
        self.cells: List[Cell] = []
        self.cells1: Dict[Tuple[int, int], Tile] = {}
        self.next_action = CollectCellAction.GetX
        self.last_ball_pos = None
        self.paddle_x = None

    def collect_cells(self):
        x = None
        y = None

        for output in self.intcode.run():
            if self.next_action == CollectCellAction.GetX:
                self.next_action = CollectCellAction.GetY
                x = output
            elif self.next_action == CollectCellAction.GetY:
                self.next_action = CollectCellAction.GetTile
                y = output
            elif self.next_action == CollectCellAction.GetTile:
                self.next_action = CollectCellAction.GetX
                if output == Tile.Block:
                    self.cells.append(Cell(x, y, output))
                elif output == Tile.HorizontalPaddle:
                    print(f'Horizontal paddle: ({x}, {y})')
                    self.paddle_x = x

                if x == -1 and y == 0:
                    print(output)

                if output == Tile.Ball:
                    print(f"Ball: ({x}, {y})")
                    diff = 0 if self.paddle_x is None else x - self.paddle_x
                    print(f'Diff: {diff}')
                    self.intcode.append_input(diff)
                    self.paddle_x = x
                else:
                    self.intcode.append_input(0)

    def count_block_tiles(self):
        return len([cell for cell in self.cells if cell.tile == Tile.Block])


with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]
    arcade = Arcade(registry)
    arcade.collect_cells()

    print(arcade.count_block_tiles())