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
    BASE = 9
    HALT = 99


class PosMode(IntEnum):
    POS = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Intcode:
    def __init__(self, registry: List[int], inputs: List[int], **kwargs):
        self.registry = registry + [0] * 10000
        self.inputs = inputs
        self.break_on_output = kwargs['break_on_output'] if 'break_on_output' in kwargs else False
        self.done = False
        self.address = 0
        self.base = 0
        self.debug = kwargs['debug'] if 'debug' in kwargs else False

    def run(self) -> Generator[int, None, None]:
        registry = self.registry

        while self.address <= len(registry):
            if self.debug:
                print(f'Address: {self.address}')
            opcode = registry[self.address]
            first_pos_mode = 0
            second_pos_mode = 0
            third_pos_mode = 0

            if len(str(opcode)) > 1:
                opcode, first_pos_mode, second_pos_mode, third_pos_mode = self.parse_opcode(opcode)

            if opcode == OpCode.ADD:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                addr2 = self.get_addr2(third_pos_mode)
                registry[addr2] = registry[addr0] + registry[addr1]
                self.address += 4
            elif opcode == OpCode.MULT:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                addr2 = self.get_addr2(third_pos_mode)
                registry[addr2] = registry[addr0] * registry[addr1]
                self.address += 4
            elif opcode == OpCode.INPUT:
                addr0 = self.get_addr0(first_pos_mode)
                registry[addr0] = self.inputs.pop(0)
                self.address += 2
            elif opcode == OpCode.OUTPUT:
                addr0 = self.get_addr0(first_pos_mode)
                self.address += 2
                yield self.registry[addr0]
                if self.break_on_output:
                    break
            elif opcode == OpCode.JUMP_TRUE:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                if self.registry[addr0] != 0:
                    self.address = self.registry[addr1]
                else:
                    self.address += 3
            elif opcode == OpCode.JUMP_FALSE:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                if self.registry[addr0] == 0:
                    self.address = self.registry[addr1]
                else:
                    self.address += 3
            elif opcode == OpCode.LESSTHAN:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                addr2 = self.get_addr2(third_pos_mode)
                registry[addr2] = 1 if registry[addr0] < registry[addr1] else 0
                self.address += 4
            elif opcode == OpCode.EQUAL:
                addr0 = self.get_addr0(first_pos_mode)
                addr1 = self.get_addr1(second_pos_mode)
                addr2 = self.get_addr2(third_pos_mode)
                registry[addr2] = 1 if registry[addr0] == registry[addr1] else 0
                self.address += 4
            elif opcode == OpCode.BASE:
                addr0 = self.get_addr0(first_pos_mode)
                self.base += registry[addr0]
                self.address += 2
                pass
            elif opcode == OpCode.HALT:
                self.done = True
                break

    def get_addr0(self, pos_mode: int):
        return self.get_address_pointer(self.address + 1, pos_mode)

    def get_addr1(self, pos_mode: int):
        return self.get_address_pointer(self.address + 2, pos_mode)

    def get_addr2(self, pos_mode: int):
        return self.get_address_pointer(self.address + 3, pos_mode)

    def parse_opcode(self, opcode: int):
        param_mode = "{:05d}".format(opcode)
        p_opcode = int(param_mode[3:5])
        first_pos_mode = int(param_mode[2])
        second_pos_mode = int(param_mode[1])
        third_pos_mode = int(param_mode[0])
        return p_opcode, first_pos_mode, second_pos_mode, third_pos_mode

    def get_address_pointer(self, index: int, pos_mode: int) -> int:
        if pos_mode == PosMode.POS:
            return self.registry[index]
        if pos_mode == PosMode.IMMEDIATE:
            return index
        if pos_mode == PosMode.RELATIVE:
            return self.registry[index] + self.base

    def append_input(self, op: int):
        self.inputs.append(op)
