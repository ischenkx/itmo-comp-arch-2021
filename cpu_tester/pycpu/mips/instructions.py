from pycpu.instruction import Instruction
from pycpu.mips.util import bindigits, twos_comp
from pycpu.processor import Processor
import numpy as np

np.warnings.simplefilter("ignore", RuntimeWarning)


def i32(val):
    return np.int32(val)


class LW(Instruction):
    def __init__(self, rs, rt, offset):
        self.rt = i32(rt)
        self.rs = i32(rs)
        self.offset = i32(offset)

    def execute(self, cpu: Processor):
        cpu.write_reg(self.rt, cpu.read_mem((cpu.read_reg(self.rs) + self.offset) >> 2))

    def __str__(self):
        return 'lw (%d, %d, %d)' % (self.offset, self.rt, self.rs)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        imm = bindigits(self.offset, 16)
        return f'100011{rs}{rt}{imm}'

    def asm(self):
        return f'lw ${self.rt}, {self.offset}(${self.rs})'


class SW(Instruction):
    def __init__(self, rs, rt, offset):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.offset = i32(offset)

    def execute(self, cpu):
        cpu.write_mem(cpu.read_reg(self.rs) + self.offset, cpu.read_reg(self.rt))

    def __str__(self):
        return 'sw (%d, %d, %d)' % (self.rs, self.rt, self.offset)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        imm = bindigits(self.offset, 16)
        return f'101011{rs}{rt}{imm}'

    def asm(self):
        return f'sw ${self.rt}, {self.offset}(${self.rs})'


class BEQ(Instruction):
    def __init__(self, rs, rt, offset):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.offset = i32(offset)

    def execute(self, cpu):
        if cpu.read_reg(self.rs) == cpu.read_reg(self.rt):
            cpu.branch(self.offset)

    def __str__(self):
        return 'beq (%d, %d, %d)' % (self.rs, self.rt, self.offset)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        imm = bindigits(self.offset, 16)
        return f'000100{rs}{rt}{imm}'

    def asm(self):
        return f'beq ${self.rs}, ${self.rt}, {self.offset}'


class ADDI(Instruction):
    def __init__(self, rs, rt, imm):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.imm = i32(imm)

    def execute(self, cpu):
        # print('addi:', self.rt, self.rs, cpu.read_reg(self.rs) + self.imm)
        # print(cpu.registers)
        cpu.write_reg(self.rt, cpu.read_reg(self.rs) + self.imm)

    def __str__(self):
        return 'addi (%d, %d, %d)' % (self.rs, self.rt, self.imm)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        imm = bindigits(self.imm, 16)
        return f'001000{rs}{rt}{imm}'

    def asm(self):
        return f'addi ${self.rt}, ${self.rs}, {self.imm}'


class ADD(Instruction):
    def __init__(self, rs, rt, rd):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.rd = i32(rd)

    def execute(self, cpu):
        cpu.write_reg(self.rd, cpu.read_reg(self.rs) + cpu.read_reg(self.rt))

    def __str__(self):
        return 'add (%d, %d, %d)' % (self.rs, self.rt, self.rd)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        rd = bindigits(self.rd, 5)
        funct = '100000'
        return f'000000{rs}{rt}{rd}00000{funct}'

    def asm(self):
        return f'add ${self.rd}, ${self.rs}, ${self.rt}'


class SUB(Instruction):
    def __init__(self, rs, rt, rd):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.rd = i32(rd)

    def execute(self, cpu):
        val1 = cpu.read_reg(self.rs)
        val2 = cpu.read_reg(self.rt)
        cpu.write_reg(self.rd, val1 - val2)

    def __str__(self):
        return 'sub (%d, %d, %d)' % (self.rs, self.rt, self.rd)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        rd = bindigits(self.rd, 5)
        funct = '100010'
        return f'000000{rs}{rt}{rd}00000{funct}'

    def asm(self):
        return f'sub ${self.rd}, ${self.rs}, ${self.rt}'


class AND(Instruction):
    def __init__(self, rs, rt, rd):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.rd = i32(rd)

    def execute(self, cpu):
        cpu.write_reg(self.rd, cpu.read_reg(self.rs) & cpu.read_reg(self.rt))

    def __str__(self):
        return 'and (%d, %d, %d)' % (self.rs, self.rt, self.rd)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        rd = bindigits(self.rd, 5)
        funct = '100100'
        return f'000000{rs}{rt}{rd}00000{funct}'

    def asm(self):
        return f'and ${self.rd}, ${self.rs}, ${self.rt}'


class OR(Instruction):
    def __init__(self, rs, rt, rd):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.rd = i32(rd)

    def execute(self, cpu):
        cpu.write_reg(self.rd, cpu.read_reg(self.rs) | cpu.read_reg(self.rt))

    def __str__(self):
        return 'or (%d, %d, %d)' % (self.rs, self.rt, self.rd)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        rd = bindigits(self.rd, 5)
        funct = '100101'
        return f'000000{rs}{rt}{rd}00000{funct}'

    def asm(self):
        return f'or ${self.rd}, ${self.rs}, ${self.rt}'


class SLT(Instruction):
    def __init__(self, rs, rt, rd):
        self.rs = i32(rs)
        self.rt = i32(rt)
        self.rd = i32(rd)

    def execute(self, cpu):
        res = int(cpu.read_reg(self.rs) < cpu.read_reg(self.rt))
        cpu.write_reg(self.rd, res)

    def __str__(self):
        return 'slt (%d, %d, %d)' % (self.rs, self.rt, self.rd)

    def binary(self):
        rs = bindigits(self.rs, 5)
        rt = bindigits(self.rt, 5)
        rd = bindigits(self.rd, 5)
        funct = '101010'
        return f'000000{rs}{rt}{rd}00000{funct}'

    def asm(self):
        return f'slt ${self.rd}, ${self.rs}, ${self.rt}'


def parse_instruction(bstr):
    op_code = bstr[:6]
    if op_code == '000000':
        # R-Type
        rs = int(bstr[6:11], 2)
        rt = int(bstr[11:16], 2)
        rd = int(bstr[16:21], 2)
        funct = bstr[-6:]
        if funct == '100000':
            # ADD
            return ADD(rs, rt, rd)
        elif funct == '100010':
            # SUB
            return SUB(rs, rt, rd)
        elif funct == '100100':
            # AND
            return AND(rs, rt, rd)
        elif funct == '100101':
            # OR
            return OR(rs, rt, rd)
        elif funct == '101010':
            # SLT
            return SLT(rs, rt, rd)
    else:
        rs = int(bstr[6:11], 2)
        rt = int(bstr[11:16], 2)
        imm = int(bstr[16:], 2)
        imm = twos_comp(imm, 16)
        if op_code == '100011':
            # LW
            return LW(rs, rt, imm)
        elif op_code == '101011':
            # SW
            return SW(rs, rt, imm)

        elif op_code == '000100':
            # BEQ
            return BEQ(rs, rt, imm)

        elif op_code == '001000':
            # ADDI
            return ADDI(rs, rt, imm)
