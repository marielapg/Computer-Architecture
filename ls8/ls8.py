#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

program = input("Enter program name: ")
program = f"examples/{program}.ls8"
file = open(program, "r")
program = []
for instruction in file:
    print(instruction)
    byte = instruction.split()[0]
    print(byte)
    if byte != '#':
        byte = int(byte, base=2)
        program.append(byte)

cpu.load(program)
cpu.run()