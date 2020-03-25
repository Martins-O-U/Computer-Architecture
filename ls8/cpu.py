"""CPU functionality."""
import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0
        self.flag = 0
        self.HALTED = False

    def ram_read(self, address):
        return self.ram[address]

    def raw_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py <filename>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as instructions:
                # read each instruction line
                for line in instructions:
                    # split each line into instructions and comments
                    split_instruction_line = line.split("#")

                    # remove whitespace
                    nums = split_instruction_line[0].strip()

                    # ignore blank lines / comment only lines
                    if len(nums) == "":
                        continue

                    # set the number to an integer of base 2
                    instruction = int(nums, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # for add operation
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # for mulitplication operation
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.fl,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
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
        PUSH = 0b01000101
        POP = 0b01000110
        SP = 7

        while not self.HALTED:
            IR = self.ram[self.PC]
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            operands = (IR & 0b11000000) >> 6

            if IR == HLT:
                print("Exiting...")
                self.HALTED = True
            elif IR == LDI:
                self.reg[operand_a] = operand_b
            elif IR == PRN:
                print(self.reg[operand_a])
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
            elif IR == PUSH:
                reg = self.ram[self.PC + 1]
                val = self.reg[reg]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val
            elif IR == POP:
                reg = self.ram[self.PC + 1]
                val = self.ram[self.reg[SP]]
                self.reg[reg] = val
                self.reg[SP] += 1

            self.PC += operands + 1
