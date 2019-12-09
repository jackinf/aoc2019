from typing import List, Generator
from enum import IntEnum


class OpCode(IntEnum):
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_TRUE = 5
    JUMP_FALSE = 6
    LESSTHAN = 7
    EQUAL = 8
    HALT = 99


class Intcode:
    def __init__(self, inputs: List[int], input_values: List[int], **kwargs):
        self.inputs = inputs
        self.input_values = input_values
        self.break_on_output = kwargs['break_on_output'] if 'break_on_output' in kwargs else False
        self.done = False
        self.instruction_pointer = 0

    def run(self) -> Generator[int, None, None]:
        inputs = self.inputs
        input_values = self.input_values

        while self.instruction_pointer <= len(inputs):
            opcode = inputs[self.instruction_pointer]
            first_pos_mode = 0
            second_pos_mode = 0

            if len(str(opcode)) > 1:
                opcode, first_pos_mode, second_pos_mode = self.parse_opcode(opcode)

            if opcode == OpCode.ADD:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                inputs[inputs[self.instruction_pointer + 3]] = first + second
                self.instruction_pointer += 4
            elif opcode == OpCode.MULT:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                inputs[inputs[self.instruction_pointer + 3]] = first * second
                self.instruction_pointer += 4
            elif opcode == OpCode.INPUT:
                inputs[inputs[self.instruction_pointer + 1]] = input_values.pop(0)
                self.instruction_pointer += 2
            elif opcode == OpCode.OUTPUT:
                value = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                yield value
                self.instruction_pointer += 2
                if self.break_on_output:
                    break
            elif opcode == OpCode.JUMP_TRUE:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                if first != 0:
                    self.instruction_pointer = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                else:
                    self.instruction_pointer += 3
            elif opcode == OpCode.JUMP_FALSE:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                if first == 0:
                    self.instruction_pointer = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                else:
                    self.instruction_pointer += 3
            elif opcode == OpCode.LESSTHAN:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                inputs[inputs[self.instruction_pointer + 3]] = 1 if first < second else 0
                self.instruction_pointer += 4
            elif opcode == OpCode.EQUAL:
                first = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 1, first_pos_mode)
                second = self.get_position_or_immediate_value(inputs, self.instruction_pointer + 2, second_pos_mode)
                inputs[inputs[self.instruction_pointer + 3]] = 1 if first == second else 0
                self.instruction_pointer += 4
            elif opcode == OpCode.HALT:
                self.done = True
                break

    def parse_opcode(self, opcode: int):
        param_mode = "{:05d}".format(opcode)
        p_opcode = int(param_mode[3:5])
        first_pos_mode = int(param_mode[2])
        second_pos_mode = int(param_mode[1])
        return p_opcode, first_pos_mode, second_pos_mode

    def get_position_or_immediate_value(self, arr: List[int], index: int, pos_mode: int) -> int:
        return arr[index] if pos_mode == 1 else arr[arr[index]]
