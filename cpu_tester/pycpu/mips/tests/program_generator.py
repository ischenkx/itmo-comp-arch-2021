import random

from pycpu.mips.instructions import *

ARITHMETIC_OPS = [
    ADD,
    SUB,
    AND,
    OR,
    SLT
]

MEM_OPS = [
    LW,
    SW
]


class ProgramGenerator(object):
    def __init__(self,
                 memory_cells,
                 amount=64,
                 reg_range=(1, 10),
            ):
        self._instructions_count = amount
        self.mem_cells = memory_cells
        self._reg_range = reg_range

    def _random_register(self):
        return random.choice(range(self._reg_range[0], self._reg_range[1] + 1))

    def _random_arithmetic_op(self):
        op = random.choice(ARITHMETIC_OPS)
        rs, rt, rd = self._random_register(), self._random_register(), self._random_register()
        return [op(rs, rt, rd)]

    def _random_mem_op(self):
        instructions = []
        mem_cell_offset = 4 * random.choice(range(0, self.mem_cells // 4))
        register = self._random_register()
        instructions.append(ADDI(0, register, 0))
        instructions.append(random.choice(MEM_OPS)(register, self._random_register(), mem_cell_offset))
        return instructions

    def _add_constants_op(self):
        const = random.randint(0, 20000)
        return [ADDI(self._random_register(), self._random_register(), const)]

    def _generate_ordered_instructions(self, cnt, _seed=1):
        instructions = []
        while len(instructions) < cnt:
            if _seed % 4 == 0:
                instructions.extend(self._add_constants_op())
            else:
                # 40% - memory op
                # 60% - arithmetic op
                if random.random() < 0.4:
                    instructions.extend(self._random_mem_op())
                else:
                    instructions.extend(self._random_arithmetic_op())
        return instructions[:cnt]

    def _generate_loop(self, inner_instructions):
        instructions = []
        iters = random.randint(1, 40)
        instructions.append(SUB(30, 30, 30))
        instructions.append(ADDI(30, 30, iters))
        instructions.append(ADDI(0, 31, 0))
        instructions.append(ADDI(31, 31, 1))
        instructions.extend(self._generate_ordered_instructions(inner_instructions))
        instructions.append(SLT(30, 31, 29))
        instructions.append(BEQ(0, 29, -inner_instructions-3))
        return instructions

    def generate(self):
        instructions = []
        _seed = 0
        # 20% - loops
        while len(instructions) < self._instructions_count:
            random.random()
            if random.random() > 0.8:
                instructions.extend(self._generate_loop(random.randint(3, 8)))
            else:
                instructions.extend(self._generate_ordered_instructions(1, _seed))
            _seed += 1
        return instructions[:self._instructions_count]