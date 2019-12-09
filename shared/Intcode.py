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


class Intcode:
    def __init__(self, registry: List[int], inputs: List[int], **kwargs):
        self.registry = registry + [0] * 1000
        self.inputs = inputs
        self.break_on_output = kwargs['break_on_output'] if 'break_on_output' in kwargs else False
        self.done = False
        self.address = 0
        self.base = 0

    def run(self) -> Generator[int, None, None]:
        registry = self.registry
        inputs = self.inputs

        while self.address <= len(registry):
            opcode = registry[self.address]
            first_pos_mode = 0
            second_pos_mode = 0
            third_pos_mode = 0

            if len(str(opcode)) > 1:
                opcode, first_pos_mode, second_pos_mode, third_pos_mode = self.parse_opcode(opcode)

            if opcode == OpCode.ADD:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                addr2 = self.get_address_pointer(registry, self.address + 3, third_pos_mode)
                registry[addr2] = registry[addr0] + registry[addr1]
                self.address += 4
            elif opcode == OpCode.MULT:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                addr2 = self.get_address_pointer(registry, self.address + 3, third_pos_mode)
                registry[addr2] = registry[addr0] * registry[addr1]
                self.address += 4
            elif opcode == OpCode.INPUT:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                registry[addr0] = inputs.pop(0)
                self.address += 2
            elif opcode == OpCode.OUTPUT:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                yield self.registry[addr0]
                self.address += 2
                if self.break_on_output:
                    break
            elif opcode == OpCode.JUMP_TRUE:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                if self.registry[addr0] != 0:
                    addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                    self.address = self.registry[addr1]
                else:
                    self.address += 3
            elif opcode == OpCode.JUMP_FALSE:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                if self.registry[addr0] == 0:
                    addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                    self.address = self.registry[addr1]
                else:
                    self.address += 3
            elif opcode == OpCode.LESSTHAN:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                addr2 = self.get_address_pointer(registry, self.address + 3, third_pos_mode)
                registry[addr2] = 1 if registry[addr0] < registry[addr1] else 0
                self.address += 4
            elif opcode == OpCode.EQUAL:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                addr1 = self.get_address_pointer(registry, self.address + 2, second_pos_mode)
                addr2 = self.get_address_pointer(registry, self.address + 3, third_pos_mode)
                registry[addr2] = 1 if registry[addr0] == registry[addr1] else 0
                self.address += 4
            elif opcode == OpCode.BASE:
                addr0 = self.get_address_pointer(registry, self.address + 1, first_pos_mode)
                self.base += registry[addr0]
                self.address += 2
                pass
            elif opcode == OpCode.HALT:
                self.done = True
                break

    def parse_opcode(self, opcode: int):
        param_mode = "{:05d}".format(opcode)
        p_opcode = int(param_mode[3:5])
        first_pos_mode = int(param_mode[2])
        second_pos_mode = int(param_mode[1])
        third_pos_mode = int(param_mode[0])
        return p_opcode, first_pos_mode, second_pos_mode, third_pos_mode

    def get_address_pointer(self, arr: List[int], index: int, pos_mode: int) -> int:
        if pos_mode == 0:
            return arr[index]
        if pos_mode == 1:
            return index
        if pos_mode == 2:
            return arr[index] + self.base
