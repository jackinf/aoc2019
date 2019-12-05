from typing import List


class Solution:
    def solve(self, inputs: List[int], input_value: int):
        i = 0
        while inputs[i] != 99 and i <= len(inputs):
            opcode = inputs[i]
            first_pos_mode = 0
            second_pos_mode = 0

            if len(str(opcode)) > 1:
                opcode, first_pos_mode, second_pos_mode = self.parse_opcode(opcode)

            if opcode == 1:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                inputs[inputs[i + 3]] = first + second
                i += 4
            elif opcode == 2:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                inputs[inputs[i + 3]] = first * second
                i += 4
            elif opcode == 3:
                inputs[inputs[i + 1]] = input_value
                i += 2
            elif opcode == 4:
                value = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                print(value)
                i += 2
            elif opcode == 5:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                if first != 0:
                    i = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                else:
                    i += 3
            elif opcode == 6:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                if first == 0:
                    i = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                else:
                    i += 3
            elif opcode == 7:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                inputs[inputs[i + 3]] = 1 if first < second else 0
                i += 4
            elif opcode == 8:
                first = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, i + 2, second_pos_mode)
                inputs[inputs[i + 3]] = 1 if first == second else 0
                i += 4

    def parse_opcode(self, opcode: int):
        param_mode = "{:05d}".format(opcode)
        p_opcode = int(param_mode[3:5])
        first_pos_mode = int(param_mode[2])
        second_pos_mode = int(param_mode[1])
        return p_opcode, first_pos_mode, second_pos_mode

    def get_position_or_immediate_value(self, arr: List[int], index: int, pos_mode: int) -> int:
        return arr[index] if pos_mode == 1 else arr[arr[index]]


sol = Solution()

print('=== TEST CASES ===')
test_case = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
sol.solve([int(x) for x in test_case.split(',')], 7)  # less than 8 outputs 999
sol.solve([int(x) for x in test_case.split(',')], 8)  # equal to 8 outputs 1000
sol.solve([int(x) for x in test_case.split(',')], 9)  # more than 8 outputs 1001

with open('input.txt', 'r') as f:
    inputs = [int(x) for x in f.readline().split(',')]
    print('=== PART 1 ===')
    sol.solve(inputs[:], 1)  # outputs answer to the first part
    print('=== PART 2 ===')
    sol.solve(inputs[:], 5)  # outputs answer to the second part
