from typing import List
from itertools import permutations

from shared.Intcode import Intcode


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in test_case.split(',')]


class Solution:
    def run(self, inputs: List[int]) -> int:
        return self.run_sequence(inputs, [4, 3, 2, 1, 0])

    def run_sequence(self, inputs: List[int], phases: List[int]) -> int:
        sol5 = Intcode()
        max_output = 0
        for permutation in permutations(phases):
            last_output = 0
            for phase in permutation:
                result1 = list(sol5.run(inputs[:], [phase, last_output]))
                last_output = result1[-1]
            max_output = max(max_output, last_output)
        return max_output


test_case_1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"  # 43210
test_case_2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"  # 54321
test_case_3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"  # 65210

sol = Solution()
print(sol.run(parse_inputs(test_case_1)))
print(sol.run(parse_inputs(test_case_2)))
print(sol.run(parse_inputs(test_case_3)))

with open('input.txt', 'r') as f:
    print(sol.run(parse_inputs(f.readline())))
