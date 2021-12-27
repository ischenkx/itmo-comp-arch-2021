from pycpu.processor import Processor


class Instruction(object):
    def execute(self, cpu: Processor):
        raise Exception("Interface call!")