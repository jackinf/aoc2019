from typing import List

from shared.Intcode import Intcode


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in test_case.split(',')]


class Solution:
    def run(self, registry: str, inputs=None) -> List[int]:
        if inputs is None:
            inputs = []
        parsed = parse_inputs(registry)
        outputs = list(Intcode(parsed, inputs).run())
        return outputs


test_case_1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
test_case_2 = "1102,34915192,34915192,7,4,7,99,0"
test_case_3 = "104,1125899906842624,99"

sol = Solution()
print(sol.run(test_case_1))
print(sol.run(test_case_2))
print(sol.run(test_case_3))

with open('input.txt', 'r') as f:
    file_input = f.readline()
    print(sol.run(file_input[:], [1]))
    print(sol.run(file_input[:], [2]))
