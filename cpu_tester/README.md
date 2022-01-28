# Overview
- Generates random tests
- Runs them in a python emulator
- Runs them in a verilog cpu
- Compares memory snapshots

# Requirements
- Python
- Numpy
- Icarus Verilog (iverilog, vvp must be in the PATH)

# How to run?
1. Clone this repo
2. Put your cpu files in the <SOURCE\_DIR (default=cpu)> (don't touch cpu_test.v)
3. (Optional) modify the config file
4. python tester.py <CONFIG_PATH (default="config.json")>


# Config
```json
{
    "cpu_test_path": "./cpu/cpu_test.v",
    "cpu_folder": "./cpu",
    "max_instructions": 200,
    "instructions_folder": "instructions_tmp_folder",
    "tests": 10000,
    "memory_cells": 10,
    "iverilog_flags": "-g2012",
    "test_build_folder": "test_build_folder",
    "registers_range": [1, 10],
    "fails_folder": "./fails",
    "workers": 4,
    "time_out": 5000,
    "memory_array_name": null,
    "registers_array_name": null,
    "instructions_array_name": null
}
```


An example of a working cpu can be found in the 'cpu' folder.