from typing import List, Generator


class Intcode:
    def run(self, inputs: List[int], input_values: List[int]) -> Generator[int, None, None]:
        i = 0
        input_value_index = 0
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
                inputs[inputs[i + 1]] = input_values[input_value_index]
                if len(input_values) != input_value_index - 1:
                    input_value_index += 1
                i += 2
            elif opcode == 4:
                value = self.get_position_or_immediate_value(inputs, i + 1, first_pos_mode)
                yield value
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
