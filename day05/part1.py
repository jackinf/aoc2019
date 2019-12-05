from typing import List


class Solution:
    def solve(self, inputs: List[int], input_value: int) -> int:
        i = 0
        while inputs[i] != 99 and i <= len(inputs):
            opcode = inputs[i]
            first_pos_mode = 0
            second_pos_mode = 0

            if len(str(opcode)) > 1:
                opcode, first_pos_mode, second_pos_mode = self.parse_opcode(opcode)

            if opcode == 1:
                first_pos = inputs[i + 1]
                second_pos = inputs[i + 2]
                output_pos = inputs[i + 3]
                a = first_pos if first_pos_mode == 1 else inputs[first_pos]
                b = second_pos if second_pos_mode == 1 else inputs[second_pos]
                inputs[output_pos] = a + b
                i += 4
            elif opcode == 2:
                first_pos = inputs[i + 1]
                second_pos = inputs[i + 2]
                output_pos = inputs[i + 3]
                a = first_pos if first_pos_mode == 1 else inputs[first_pos]
                b = second_pos if second_pos_mode == 1 else inputs[second_pos]
                inputs[output_pos] = a * b
                i += 4
            elif opcode == 3:
                pos = inputs[i + 1]
                inputs[pos] = input_value
                i += 2
            elif opcode == 4:
                pos = inputs[i + 1]
                print(inputs[pos] if first_pos_mode == 0 else pos)
                i += 2

    def parse_opcode(self, opcode: int):
        param_mode = "{:05d}".format(opcode)
        p_opcode = int(param_mode[3:5])
        first_pos_mode = int(param_mode[2])
        second_pos_mode = int(param_mode[1])
        return p_opcode, first_pos_mode, second_pos_mode


with open('input.txt', 'r') as f:
    inputs = [int(x) for x in f.readline().split(',')]
    input_value = 1

    sol = Solution()
    sol.solve(inputs, input_value)
