from enum import IntEnum
from time import sleep
from typing import Tuple, Dict, List

from shared.Intcode import Intcode


class MoveDirection(IntEnum):
    North = 1,
    South = 2,
    West = 3,
    East = 4


class TurnDirection(IntEnum):
    Left90Deg = 0,
    Right90Deg = 1


class RobotAction(IntEnum):
    Paint = 1,
    TurnAndMove = 2


class Color(IntEnum):
    Black = 0
    White = 1


class Grid:
    def __init__(self):
        self.painted_squares: Dict[Tuple[int, int], int] = {}

    def get_square_color(self, x: int, y: int):
        if (x, y) in self.painted_squares:
            return self.painted_squares[(x, y)]
        return 0

    def paint(self, x: int, y: int, color: int):
        self.painted_squares[(x, y)] = color

    def get_squares_painted_count(self):
        return len(self.painted_squares)

    def print_painted_text(self):
        keys = self.painted_squares.keys()
        x_offset = abs(min([key[0] for key in keys]))
        y_offset = abs(min([key[1] for key in keys]))
        len_x = max([key[0] for key in keys]) + 1
        len_y = max([key[1] for key in keys]) + 1
        arr = []
        for x in range(len_x + x_offset):
            arr.append([])
            for y in range(len_y + y_offset):
                arr[-1].append("  ")

        print(f'Len x with offset: {len_x + x_offset}')
        print(f'Len y with offset: {len_y + y_offset}')
        for k in self.painted_squares.keys():
            x = k[0]
            y = k[1]
            try:
                arr[x + x_offset][y + y_offset] = "▓▓" if self.get_square_color(x, y) == 1 else "  "
            except:
                print(f'Caught on x:{x + x_offset} and y:{y + y_offset}')

        arr = [*zip(*arr)]  # transpose
        for x in arr:
            print(''.join(x))
            # print('\n')


class PaintRobot:
    def __init__(self, registry: List[int], grid: Grid, starting_color: Color):
        self.x = 0
        self.y = 0
        self.intcode = Intcode(registry, [starting_color], break_on_output=False, debug=False)
        self.move_direction: MoveDirection = MoveDirection.North
        self.next_action = RobotAction.Paint
        self.grid = grid

    def turn(self, turn_direction: TurnDirection):
        if self.move_direction == MoveDirection.North:
            self.move_direction = MoveDirection.West if turn_direction == TurnDirection.Left90Deg else MoveDirection.East
        elif self.move_direction == MoveDirection.West:
            self.move_direction = MoveDirection.South if turn_direction == TurnDirection.Left90Deg else MoveDirection.North
        elif self.move_direction == MoveDirection.South:
            self.move_direction = MoveDirection.East if turn_direction == TurnDirection.Left90Deg else MoveDirection.West
        elif self.move_direction == MoveDirection.East:
            self.move_direction = MoveDirection.North if turn_direction == TurnDirection.Left90Deg else MoveDirection.South

    def step(self):
        if self.move_direction == MoveDirection.North:
            self.y -= 1
        elif self.move_direction == MoveDirection.South:
            self.y += 1
        if self.move_direction == MoveDirection.West:
            self.x -= 1
        elif self.move_direction == MoveDirection.East:
            self.x += 1

    def run(self):
        for output in self.intcode.run():
            if self.next_action == RobotAction.Paint:
                self.grid.paint(self.x, self.y, output)
                self.next_action = RobotAction.TurnAndMove
            elif self.next_action == RobotAction.TurnAndMove:
                self.turn(output)
                self.step()
                self.next_action = RobotAction.Paint
                ground_color = self.grid.get_square_color(self.x, self.y)
                self.intcode.append_input(ground_color)


with open('test-case-2.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]
    grid1 = Grid()
    robot1 = PaintRobot(registry, grid1, Color.Black)
    robot1.run()
    print("PART 1")
    print(grid1.get_squares_painted_count())

    print("PART 2")
    grid2 = Grid()
    robot2 = PaintRobot(registry, grid2, Color.White)
    robot2.run()
    grid2.print_painted_text()

