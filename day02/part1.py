from typing import List


def solve(inputs: List[int]) -> int:
    for i in range(0, len(inputs), 4):
        action = inputs[i]
        first_pos = inputs[i+1]
        second_pos = inputs[i+2]
        output_pos = inputs[i+3]

        if action == 99:
            return inputs[0]
        elif action == 1:
            inputs[output_pos] = inputs[first_pos] + inputs[second_pos]
        elif action == 2:
            inputs[output_pos] = inputs[first_pos] * inputs[second_pos]
        else:
            raise Exception("Unknown action")


with open('input.txt', 'r') as f:
    file_inputs = [int(x) for x in f.readline().split(',')]
    file_inputs[1] = 12
    file_inputs[2] = 2
    print(solve(file_inputs))
