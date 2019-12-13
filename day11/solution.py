from enum import IntEnum
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


class PaintRobot:
    def __init__(self, registry: List[int], grid: Grid):
        self.x = 0
        self.y = 0
        self.intcode = Intcode(registry, [grid.get_square_color(self.x, self.y)], break_on_output=True)
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
        while not self.intcode.done:
            output = next(self.intcode.run())
            if self.next_action == RobotAction.Paint:
                self.grid.paint(self.x, self.y, output)
                self.next_action = RobotAction.TurnAndMove
            elif self.next_action == RobotAction.TurnAndMove:
                self.turn(output)
                self.step()
                self.next_action = RobotAction.Paint
                ground_color = self.grid.get_square_color(self.x, self.y)
                self.intcode.append_input(ground_color)


with open('input.txt', 'r') as f:
    registry = [int(x) for x in f.readline().split(',')]
    grid = Grid()
    robot = PaintRobot(registry, grid)
    robot.run()
    print(grid.get_squares_painted_count())