from typing import List

from day02.part1 import solve_part1


def solve_part2(inputs: List[int]) -> int:
    for i in range(0, 100):
        for j in range(0, 100):
            copied_inputs = inputs[:]
            copied_inputs[1] = i
            copied_inputs[2] = j
            solution = solve_part1(copied_inputs)
            if solution == 19690720:
                return 100 * i + j
    return -1


with open('test-case-2.txt', 'r') as f:
    file_inputs = [int(x) for x in f.readline().split(',')]
    print(f'Solution to part 2: {solve_part2(file_inputs)}')
