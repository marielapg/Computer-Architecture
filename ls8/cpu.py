"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
    LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)

            if instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2

            elif instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                self.reg[reg_num] = value

                self.pc += 3

            elif instruction == MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu("MUL", reg_a, reg_b)

                self.pc += 3

            elif instruction == ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu("ADD", reg_a, reg_b)

                self.pc += 3

            elif instruction == PUSH:
                reg_num = self.ram[self.pc + 1]
                self.push(self.reg[reg_num])
                self.pc += 2

            elif instruction == POP:
                reg_num = self.ram[self.pc + 1]
                self.pop()
                self.pc += 2

            elif instruction == CALL:
                reg_num = self.ram[self.pc + 1]
                self.push(self.pc + 2)
                self.pc = self.reg[reg_num]

            elif instruction == RET:
                self.pc = self.pop()

            elif instruction == HLT:

                halted = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def push(self, value):
        self.sp -= 1
        self.ram[self.sp] = value

    def pop(self):
        if self.sp < len(self.ram) - 1:
            value = self.ram[self.sp]
            self.sp += 1
            return value