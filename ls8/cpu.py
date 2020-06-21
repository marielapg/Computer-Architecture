"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = len(self.ram) - 1
        self.L = False
        self.G = False
        self.E = False

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,10
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            # 10000010, # LDI R0,10
            # 00000000,
            # 0b00001010,
            # 10000010, # LDI R1,20
            # 0b00000001,
            # 0b00010100,
            # 10000010, # LDI R2,TEST1
            # 0b00000010,
            # 0b00010011,
            # 10100111, # CMP R0,R1
            # 00000000,
            # 0b00000001,
            # 0b01010101, # JEQ R2
            # 0b00000010,
            # 10000010, # LDI R3,1
            # 0b00000011,
            # 0b00000001,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # # TEST1 (address 19):
            # 10000010, # LDI R2,TEST2
            # 0b00000010,
            # 0b00100000,
            # 10100111, # CMP R0,R1
            # 00000000,
            # 0b00000001,
            # 0b01010110, # JNE R2
            # 0b00000010,
            # 10000010, # LDI R3,2
            # 0b00000011,
            # 0b00000010,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # # TEST2 (address 32):
            # 10000010, # LDI R1,10
            # 0b00000001,
            # 0b00001010,
            # 10000010, # LDI R2,TEST3
            # 0b00000010,
            # 0b00110000,
            # 10100111, # CMP R0,R1
            # 00000000,
            # 0b00000001,
            # 0b01010101, # JEQ R2
            # 0b00000010,
            # 10000010, # LDI R3,3
            # 0b00000011,
            # 0b00000011,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # # TEST3 (address 48):
            # 10000010, # LDI R2,TEST4
            # 0b00000010,
            # 0b00111101,
            # 10100111, # CMP R0,R1
            # 00000000,
            # 0b00000001,
            # 0b01010110, # JNE R2
            # 0b00000010,
            # 10000010, # LDI R3,4
            # 0b00000011,
            # 0b00000100,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # # TEST4 (address 61):
            # 10000010, # LDI R3,5
            # 0b00000011,
            # 0b00000101,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # 10000010, # LDI R2,TEST5
            # 0b00000010,
            # 0b01001001,
            # 0b01010100, # JMP R2
            # 0b00000010,
            # 0b01000111, # PRN R3
            # 0b00000011,
            # # TEST5 (address 73):
            # 0b00000001 # HLT

        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
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
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)

            if  instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc += 3

            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                print( self.reg[reg_num])
                self.pc += 2

        
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

            elif instruction == CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                print("PRINT", self.reg[reg_num])

                comp_a = self.reg[reg_a]
                comp_b = self.reg[reg_b]

                if comp_a < comp_b:
                    self.L = True
                elif comp_a > comp_b:
                    self.G = True

                if comp_a == comp_b:
                    self.E = True
                else:
                    self.E = False

                self.pc += 3

            elif instruction == JMP:
                reg_num = self.ram[self.pc + 1]
                self.pc = self.reg[reg_num]

            elif instruction == JEQ:
                if self.E == True:
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2

            elif instruction == JNE:
                if self.E == False:
                    reg_num = self.ram[self.pc + 1]
                    self.pc = self.reg[reg_num]
                else:
                    self.pc += 2;    

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
            
    def comp(self):
        reg_a = 0
        reg_b = 1
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    def jmp(self):
        reg_address = self.ram[self.pc + 1]
        self.pc = self.reg[reg_address]

    def jeq(self):
        if self.fl == 1:
            reg_address = self.ram[self.pc + 1]
            self.pc = self.reg[reg_address]
        else:
            self.pc += 2

    def jne(self):
        if self.fl != 1:
            reg_address = self.ram[self.pc + 1]
            self.pc = self.reg[reg_address]
        else:
            self.pc += 2
        