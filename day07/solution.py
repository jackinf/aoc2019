from typing import List
from itertools import permutations

from shared.Intcode import Intcode


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in test_case.split(',')]


class Solution:
    def run_part1(self, inputs: List[int]) -> int:
        max_output = 0
        for permutation in permutations([4, 3, 2, 1, 0]):
            last_output = 0
            for phase in permutation:
                result = list(Intcode(inputs[:], [phase, last_output]).run())
                last_output = result[-1]
            max_output = max(max_output, last_output)
        return max_output

    def run_part2(self, inputs: List[int]) -> int:
        max_output = 0
        for permutation in permutations([5, 6, 7, 8, 9]):
            last_output = 0
            intcodes = []
            for phase in permutation:
                intcodes.append(Intcode(inputs[:], [phase], break_on_output=True))

            while any(intcode.done is False for intcode in intcodes):
                for intcode in intcodes:
                    intcode.input_values.append(last_output)
                    result = list(intcode.run())
                    if len(result) > 0:
                        last_output = result[-1]
            max_output = max(max_output, last_output)
        return max_output


sol = Solution()

print("\nTEST CASES FOR PART 1")
test_case_1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"  # 43210
test_case_2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"  # 54321
test_case_3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"  # 65210

print(sol.run_part1(parse_inputs(test_case_1)))
print(sol.run_part1(parse_inputs(test_case_2)))
print(sol.run_part1(parse_inputs(test_case_3)))

print("\nTEST CASES FOR PART 2")
test_case_4 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
test_case_5 = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
print(sol.run_part2(parse_inputs(test_case_4)))
print(sol.run_part2(parse_inputs(test_case_5)))

with open('input.txt', 'r') as f:
    parsed_inputs = parse_inputs(f.readline())
    print("\nPART 1")
    print(sol.run_part1(parsed_inputs))
    print("\nPART 2")
    print(sol.run_part2(parsed_inputs))
