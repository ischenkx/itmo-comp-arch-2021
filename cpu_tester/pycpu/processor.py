class Processor(object):
    def write_mem(self, addr, value):
        raise Exception("Interface call!")

    def write_reg(self, addr, value):
        raise Exception("Interface call!")

    def read_mem(self, addr) -> int:
        raise Exception("Interface call!")

    def read_reg(self, addr) -> int:
        raise Exception("Interface call!")

    def branch(self, pc):
        raise Exception("Interface call!")