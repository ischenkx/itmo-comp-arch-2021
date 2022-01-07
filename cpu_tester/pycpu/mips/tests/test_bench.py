import os
import queue
import threading
import random

from pycpu.mips.mips import MIPS
from pycpu.mips.tests.config import Config
from pycpu.mips.tests.program_generator import ProgramGenerator
from pycpu.mips.tests.verilog_api import VerilogApi


class TestBench(object):

    class Job(object):
        def __init__(self, instructions, id):
            self.instructions = instructions
            self._id = id

        def get_id(self):
            return self._id

        def get_instructions(self):
            return self.instructions

    class Result(object):
        def __init__(
                self,
                job_id,
                ok=True,
                message=None,
                source=None,
                memory_snapshots=(None, None),
        ):
            self.job_id = job_id
            self.source = source
            self.reason = message
            self.memory_snapshots = memory_snapshots
            self.ok = ok

        def is_ok(self):
            return self.ok

    class Tester(threading.Thread):
        def __init__(self, _input: queue.Queue, _output: queue.Queue, _config: Config, *args, **kwargs):
            self._input = _input
            self._output = _output
            self._lock = threading.Lock()
            self._killed = False
            self._config = _config

            super().__init__(*args, **kwargs)

        def kill(self):
            self._lock.acquire()
            self._killed = True
            self._lock.release()

        def is_killed(self):
            self._lock.acquire()
            _killed = self._killed
            self._lock.release()
            return _killed

        def run(self):
            cpu = MIPS(
                mem_size=self._config.memory_cells,
            )

            verilog = VerilogApi(
                test_path=self._config.cpu_test_path,
                build_folder_path=self._config.test_build_folder,
                iverilog_build_flags=f'{self._config.iverilog_flags} -I {self._config.cpu_folder}',
                max_instructions=self._config.max_instructions,
                instructions_folder_path=self._config.instructions_folder
            )

            while True:
                if self.is_killed():
                    return
                try:
                    job = self._input.get(timeout=3, block=True)
                except Exception:
                    continue

                try:
                    cpu.reset()
                    cpu.set_instructions(job.get_instructions())
                    cpu.run(time_out=self._config.time_out)
                except Exception as ex:
                    res = TestBench.Result(job.get_id(), ok=False, message=f'unexpected error: {ex}', source='cpu')
                    self._output.put(res, block=False)
                    self._input.task_done()
                    continue

                try:
                    verilog_memory = verilog.run(job.get_instructions(), time_out=self._config.time_out)
                except Exception as ex:
                    res = TestBench.Result(job.get_id(), ok=False, message=f'unexpected error: {ex}', source='verilog')
                    self._output.put(res, block=False)
                    self._input.task_done()
                    continue

                failed = False
                for i in range(self._config.memory_cells):
                    cpu_cell = cpu.read_mem(i)
                    verilog_cell = verilog_memory[i]
                    if cpu_cell != verilog_cell:
                        failed = True
                        break

                if failed:
                    res = TestBench.Result(job.get_id(),
                                           ok=False,
                                           message='memory check failed',
                                           source='cpu+verilog',
                                           memory_snapshots=(cpu.memory.copy(), verilog_memory.copy())
                                        )
                else:
                    res = TestBench.Result(job.get_id())
                self._output.put(res)
                self._input.task_done()

    def __init__(self, config=None):
        if config is None:
            config = Config.from_file('')

        self._config = config

    def _save_failed_program(self, instructions):
        if not os.path.isdir(self._config.fails_folder):
            os.mkdir(self._config.fails_folder)

        _bin = '\n'.join(map(lambda i: i.binary(), instructions))
        _asm = '\n'.join(map(lambda i: i.asm(), instructions))

        tag = random.randint(0, 10000000)

        # dumping binaries
        with open(os.path.join(self._config.fails_folder, f'{tag}_bin'), 'w') as f:
            f.write(_bin)
        # dumping asm
        with open(os.path.join(self._config.fails_folder, f'{tag}_asm'), 'w') as f:
            f.write(_asm)
        return tag

    def run(self):
        generator = ProgramGenerator(memory_cells=self._config.memory_cells)
        _input = queue.Queue()
        _output = queue.Queue()

        workers = []
        for i in range(self._config.workers):
            w = TestBench.Tester(_input, _output, self._config)
            workers.append(w)
            w.start()
        print(f'[LOG] starting (workers={self._config.workers})')
        tasks_to_do = self._config.tests
        tasks_enqueued = 0

        jobs = {}

        passed = 0
        failed = 0
        total = self._config.tests

        job_id = 0

        while tasks_to_do > 0:
            while not _output.empty():
                if (failed + passed) % 100 == 99:
                    print(f'[LOG] total={total} failed={failed} passed={passed}')

                res: TestBench.Result = _output.get(block=False)
                instructions = jobs[res.job_id]
                del jobs[res.job_id]

                if res.is_ok():
                    passed += 1
                else:
                    try:
                        tag = self._save_failed_program(instructions)
                    except Exception as ex:
                        print('failed to save a file:', ex)
                        tag = '<UNKNOWN>'

                    print(
                        f'[FAILURE] source=\'{res.source}\' message=\'{res.reason}\'\n'
                        f'cpu_memory={res.memory_snapshots[0]}\n'
                        f'verilog_memory={res.memory_snapshots[1]}\n'
                        f'tag={tag}\n'
                        f'failed={failed} passed={passed}'
                        f''
                    )

                    failed += 1
                tasks_to_do -= 1
            if tasks_enqueued < total:
                instructions = generator.generate()
                job_id += 1
                jobs[job_id] = instructions
                _input.put(TestBench.Job(instructions, job_id))

        for w in workers:
            w.kill()

