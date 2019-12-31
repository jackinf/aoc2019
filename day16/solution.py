import math
from typing import List

import numpy as np


def read_inputs(file_name: str):
    with open(file_name, 'r') as f:
        return [int(x) for x in f.readline()]


def calculate_pattern(position: int, min_element_count: int):
    initial_pattern = [0, 1, 0, -1]
    pattern = np.repeat(initial_pattern, position+1)
    if len(pattern) <= min_element_count:
        pattern = np.tile(pattern, math.ceil(min_element_count // len(pattern)) + 1)
    return pattern


def calculate_phase(numbers: List[int]) -> List[int]:
    results = []
    n = len(numbers)
    for i in range(n):
        pattern = calculate_pattern(i, n)
        res = 0
        for j in range(len(numbers)):
            pattern_val = pattern[1+j]
            number_val = numbers[j]
            res += pattern_val * number_val
        results.append(int(f'{res}'[-1]))
    return results


if __name__ == "__main__":
    inputs = read_inputs('test-case-2.txt')

    phase_inputs = np.copy(inputs)
    for _ in range(100):
        phase_inputs = calculate_phase(phase_inputs)
    print(phase_inputs[0:8])