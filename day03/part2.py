import sys
from typing import List, Tuple

from day03.part1 import direction_str_to_list, get_lines


def get_least_steps(lines1: List[Tuple[int, int, int, int, int]], lines2: List[Tuple[int, int, int, int, int]]) -> int:
    steps = sys.maxsize
    for curr_line1 in lines1:
        x1_start, y1_start, x1_end, y1_end, line1_steps = curr_line1

        for curr_line2 in lines2:
            x2_start, y2_start, x2_end, y2_end, line2_steps = curr_line2

            if x1_start == x1_end and x2_start != x2_end:  # is 1st line is vertical and second is not vertical
                x1 = x1_start  # = x1_end
                y2 = y2_start  # = y2_end
                if (x2_start < x1 < x2_end or x2_start > x1 > x2_end) and (y1_start < y2 < y1_end or y1_start > y2 > y1_end):
                    total_line1_steps = line1_steps - abs(y1_end - y2_end)
                    total_line2_steps = line2_steps - abs(x2_end - x1_end)
                    total_steps = total_line1_steps + total_line2_steps
                    steps = min(steps, total_steps)
            elif x1_start != x1_end and x2_start == x2_end:    # is 1st line is not vertical and second is vertical
                x2 = x2_start  # = x2_end
                y1 = y1_start  # = y1_end
                if (x1_start < x2 < x1_end or x1_start > x2 > x1_end) and (y2_start < y1 < y2_end or y2_start > y1 > y2_end):
                    total_line1_steps = line1_steps - abs(x1_end - x2_end)
                    total_line2_steps = line2_steps - abs(y2_end - y1_end)
                    total_steps = total_line1_steps + total_line2_steps
                    steps = min(steps, total_steps)
    return steps


def solution(inputs: dict):
    wire1_directions = direction_str_to_list(inputs["wire1"])
    wire2_directions = direction_str_to_list(inputs["wire2"])
    lines1 = get_lines(wire1_directions)
    lines2 = get_lines(wire2_directions)
    return get_least_steps(lines1, lines2)


test1_inputs = {
    "wire1": "R8,U5,L5,D3",
    "wire2": "U7,R6,D4,L4"
}
test2_inputs = {
    "wire1": "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    "wire2": "U62,R66,U55,R34,D71,R55,D58,R83"
}
test3_inputs = {
    "wire1": "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    "wire2": "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
}


with open('test-case-2.txt', 'r') as f:
    line1 = f.readline()
    line2 = f.readline()
    task_input = {
        "wire1": line1,
        "wire2": line2
    }
    result = solution(task_input)  # managed to get a correct solution though example numbers don't match for some reason
    print(result)