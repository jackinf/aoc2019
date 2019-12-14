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
        self.intcode = Intcode(registry, [])
        self.cells: List[Cell] = []
        self.cells1: Dict[Tuple[int, int], Tile] = {}
        self.next_action = CollectCellAction.GetX

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
                self.cells.append(Cell(x, y, output))
                self.cells1[(x, y)] = output

    def count_block_tiles(self):
        return len([cell for cell in self.cells if cell.tile == Tile.Block])


with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]
    arcade = Arcade(registry)
    arcade.collect_cells()
    print(arcade.count_block_tiles())