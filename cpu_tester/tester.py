import json
import os
import random
import sys

from pycpu.mips.tests.config import Config
from pycpu.mips.tests.test_bench import TestBench

if __name__ == '__main__':
    args = sys.argv[1:]
    config_path = 'config.json'
    if len(args) > 0:
        config_path = args[0]

    config = Config.from_file(config_path)
    test_bench = TestBench(config)
    test_bench.run()


