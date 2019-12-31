from typing import List, Generator
from shared.Intcode import Intcode

sol = Intcode()

print('=== TEST CASES ===')
test_case = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
sol.run([int(x) for x in test_case.split(',')], [7])  # less than 8 outputs 999
sol.run([int(x) for x in test_case.split(',')], [8])  # equal to 8 outputs 1000
sol.run([int(x) for x in test_case.split(',')], [9])  # more than 8 outputs 1001

with open('test-case-2.txt', 'r') as f:
    inputs = [int(x) for x in f.readline().split(',')]
    print('=== PART 1 ===')
    solution1 = sol.run(inputs[:], [1])
    print(list(solution1))

    print('=== PART 2 ===')
    solution2 = sol.run(inputs[:], [5])
    print(list(solution2))
