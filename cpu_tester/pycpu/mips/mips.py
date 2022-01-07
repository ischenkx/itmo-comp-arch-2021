import datetime
import time

from pycpu.mips.instructions import *


class MIPS(Processor):
    def __init__(self,
                 mem_size=2048,
                 reg_cnt=32):
        self._mem_size = mem_size
        self._reg_cnt = reg_cnt
        self.memory = []
        self.registers = []
        self.instructions = []
        self._pc = 0
        self._branch_offset = None
        self.reset()

    def reset(self):
        self.memory = [0] * self._mem_size
        self.registers = [0] * self._reg_cnt
        self.instructions = []
        self._pc = 0
        self._branch_offset = None

    def set_instructions(self, instructions):
        self.instructions = instructions
        self._pc = 0
        self._branch_offset = None

    def _current_instruction(self):
        return self.instructions[self._pc]

    def _set_pc(self, pc):
        self._pc = pc

    def _next_instruction(self):
        _inst = self._pc + 1
        if self._branch_offset is not None:
            _inst = self._pc + self._branch_offset + 1
            self._branch_offset = None
        self._set_pc(_inst)

    def write_mem(self, addr, value):
        self.memory[addr >> 2] = value

    def write_reg(self, addr, value):
        self.registers[addr] = value

    def read_mem(self, addr):
        return self.memory[addr]

    def read_reg(self, addr):
        return self.registers[addr]

    def branch(self, offset):
        self._branch_offset = offset

    # time_out - milliseconds
    def run(self, time_out=None):
        start_time = datetime.datetime.now()

        while 0 <= self._pc < len(self.instructions):
            if time_out is not None:
                now = datetime.datetime.now()
                if (now - start_time).total_seconds() >= time_out / 1000:
                    raise TimeoutError('mips processor timeout...')
            self._current_instruction().execute(self)
            self._next_instruction()


