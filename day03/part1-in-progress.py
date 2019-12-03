import sys
from typing import List, Tuple


def direction_str_to_list(direction_str: str) -> List[Tuple[str, int]]:
    """
    Converts string to more friendly format to manipulate
    :param direction_str: a single string, separated by commas and each value has letter following with numbers
    :return: each element is a tulpe where first element is a direction and second is a number of steps
    """
    return [(x[0], int(x[1:])) for x in direction_str.split(',')]


def walk_in_grid(direction_list: List[Tuple[str, int]]) -> List[Tuple[int, int]]:
    visited_coordinates = []
    curr_x = 0
    curr_y = 0
    for i in range(len(direction_list)):
        direction, steps = direction_list[i]
        for step in range(steps):
            if direction == "R":
                curr_x += 1
            if direction == "L":
                curr_x -= 1
            if direction == "U":
                curr_y += 1
            if direction == "D":
                curr_y -= 1
            visited_coordinates.append((curr_x, curr_y))
    return visited_coordinates


def get_lines(direction_list: List[Tuple[str, int]]) -> List[Tuple[int, int, int, int]]:
    lines = []
    curr_x = 0
    curr_y = 0
    for i in range(len(direction_list)):
        direction, steps = direction_list[i]
        new_x = None
        new_y = None
        if direction == "R":
            new_x = curr_x + steps
            new_y = curr_y
        if direction == "L":
            new_x = curr_x - steps
            new_y = curr_y
        if direction == "U":
            new_x = curr_x
            new_y = curr_y + steps
        if direction == "D":
            new_x = curr_x
            new_y = curr_y - steps
        if new_x is None or new_y is None:
            raise Exception("new_x or new_y is missing")
        lines.append((curr_x, curr_y, new_x, new_y))
        curr_x, curr_y = new_x, new_y
    return lines


def get_intersections_between_lines(lines1: List[Tuple[int, int, int, int]], lines2: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int]]:
    smallest_distance = sys.maxsize
    results = []
    for curr_line1 in lines1:
        x1_start, y1_start, x1_end, y1_end = curr_line1
        line1_horizontal = True if x1_start == x1_end else False

        for curr_line2 in lines2:
            x2_start, y2_start, x2_end, y2_end = curr_line2
            line2_horizontal = True if x2_start == x2_end else False

            if line1_horizontal == line2_horizontal:
                continue

            if line1_horizontal:
                x1 = x1_start  # = x1_end
                y2 = y2_start  # = y2_end
                if x2_start < x1 < x2_end and y1_start < y2 < y1_end or x2_start > x1 > x2_end and y1_start > y2 > y1_end:
                    px, py = abs(x1), abs(y2)
                    smallest_distance = min(smallest_distance, px + py)
                    results.append((px, py, px + py))
            else:
                x2 = x2_start  # = x2_end
                y1 = y1_start  # = y1_end
                if x1_start < x2 < x1_end and y2_start < y1 < y2_end or x1_start > x2 > x1_end and y2_start > y1 > y2_end:
                    px, py = abs(x2), abs(y1)
                    smallest_distance = min(smallest_distance, px + py)
                    results.append((px, py, px + py))
    return smallest_distance


def calculate_manhattan_distance(x: int, y: int):
    return abs(x + y)


def get_distance_to_closest_intersection(wire1: List[Tuple[int, int]], wire2: List[Tuple[int, int]]) -> int:
    smallest_distance = sys.maxsize
    for wire1_coord in wire1:
        for wire2_coord in wire2:
            x1, y1 = wire1_coord
            x2, y2 = wire2_coord
            if x1 == x2 and y1 == y2:
                distance = calculate_manhattan_distance(x1, y1)
                if distance < smallest_distance:
                    smallest_distance = distance
    return smallest_distance


def solution1(inputs: dict) -> int:
    wire1_directions = direction_str_to_list(inputs["wire1"])
    wire2_directions = direction_str_to_list(inputs["wire2"])
    wire1_visited_locations = walk_in_grid(wire1_directions)
    wire2_visited_locations = walk_in_grid(wire2_directions)
    end_result = get_distance_to_closest_intersection(wire1_visited_locations, wire2_visited_locations)
    return end_result


def solution2(inputs: dict):
    wire1_directions = direction_str_to_list(inputs["wire1"])
    wire2_directions = direction_str_to_list(inputs["wire2"])
    lines1 = get_lines(wire1_directions)
    lines2 = get_lines(wire2_directions)
    print(lines1)
    intersections = get_intersections_between_lines(lines1, lines2)
    return intersections


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

with open('input.txt', 'r') as f:
    line1 = f.readline()
    line2 = f.readline()
    task_input = {
        "wire1": line1,
        "wire2": line2
    }
    result = solution2(task_input)  # managed to get a correct solution though example numbers don't match for some reason
    print(result)
