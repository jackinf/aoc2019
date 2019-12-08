from typing import List
from day05.solution import Solution as Solution5


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in test_case.split(',')]


# NB! Unsolved
class Solution():
    def run(self, inputs: List[int]) -> int:
        return self.run_sequence(inputs, [4, 3, 2, 1, 0])

    def run_sequence(self, inputs: List[int], sequence: List[int]) -> int:
        sol5 = Solution5()
        last_output = 0
        for sequence_input in sequence:
            raise Exception("I have no idea how to pass 2 inputs where solution accepts only 1 input")
            # result1 = sol5.solve(inputs[:], last_output)
            # result2 = sol5.solve(inputs[:], sequence_input)
            # last_output = list(result2)[-1]
        return last_output


test_case_1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"

sol = Solution()
print(sol.run(parse_inputs(test_case_1)))