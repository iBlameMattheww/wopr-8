PSR_Z                   = 0 
PSR_C                   = 1
PSR_STACK_OVERFLOW      = 2
PSR_STACK_UNDERFLOW     = 3
PSR_ILLEGAL_INSTRUCTION = 4
PSR_HALTED              = 5
PSR_ILLEGAL_MEMORY      = 6
PSR_RESERVED            = 7


OP_HALT     = 0 
OP_NOP      = 1
OP_CMP      = 2
OP_JNZ      = 3
OP_JZ       = 4
OP_JMP      = 5
OP_SHIFT    = 6
OP_NOT      = 7 
OP_XORI     = 8
OP_XOR      = 9
OP_ORI      = 10
OP_OR       = 11
OP_ANDI     = 12
OP_AND      = 13
OP_MOVE     = 14
OP_STI      = 15
OP_STORE    = 16
OP_LDI      = 17
OP_LOAD     = 18
OP_SUB      = 19
OP_ADDI     = 20
OP_ADD      = 21
OP_RET      = 22
OP_CALL     = 23
OP_POP      = 24
OP_PUSH     = 25


REG_MASK = 0xFF
PC_MASK  = 0x7FF


RAM_SIZE    = 256
ROM_SIZE    = 2048


STACK_TOP = 0xDF 
STACK_MIN = 0x80
MMIO_BASE = 0xE0


R_OPS = {
    OP_HALT,
    OP_NOP,
    OP_CMP,
    OP_SHIFT,
    OP_NOT,
    OP_XOR,
    OP_OR,
    OP_AND,
    OP_MOVE,
    OP_STORE,
    OP_LOAD,
    OP_SUB,
    OP_ADD,
    OP_POP,
    OP_PUSH,
}


I_OPS = {
    OP_XORI,
    OP_ORI,
    OP_ANDI,
    OP_STI,
    OP_LDI,
    OP_ADDI,
}


J_OPS = {
    OP_JNZ,
    OP_JZ,
    OP_JMP,
    OP_RET,
    OP_CALL,
}


class WOPR_8:


    def __init__(self):
        self.regs   = [0] * 8           # R0-R7 8bit 
        self.pc     = 0                 # 11bit PC
        self.sp     = STACK_TOP         # next free stack byte
        self.psr    = 0                 # 8bit processor status register
        self.ram    = [0] * RAM_SIZE    # 256 bytes data memory
        self.rom    = [0] * ROM_SIZE    # 2048 x 16bit instructions
        self.halted = False


    def set_flag(self, bit, value):
        if value:
            self.psr |= (1 << bit)
        else:
            self.psr &= ~(1 << bit)


    def get_flag(self, bit):
        return (self.psr >> bit) & 1


    def fetch(self):
        instruction = self.rom[self.pc]
        return instruction


    def decode(self, instruction):
        opcode = instruction >> 11 
    
        if opcode in R_OPS:
            return self.decode_type_r(opcode, instruction) 

        elif opcode in J_OPS:
            return self.decode_type_j(opcode, instruction)

        elif opcode in I_OPS:
            return self.decode_type_i(opcode, instruction)

        else:
            self.set_flag(PSR_ILLEGAL_INSTRUCTION, True)
            self.halted = True
            self.set_flag(PSR_HALTED, True)
            return None

    
    def decode_type_r(self, opcode, instruction):
        rd = (instruction >> 8) & 0b111 
        rs = (instruction >> 5) & 0b111
        
        shamt = (instruction >> 2) & 0b111 
        dir = (instruction >> 1) & 0b1 

        return {
            "instruction": instruction,
            "opcode": opcode,
            "rd": rd,
            "rs": rs,
            "shamt": shamt,
            "dir": dir,
            "immediate": None,
            "address": None
        }


    def decode_type_j(self, opcode, instruction):
        address = instruction & 0b11111111111

        return {
            "instruction": instruction,
            "opcode": opcode,
            "rd": None,
            "rs": None,
            "shamt": None,
            "dir": None,
            "immediate": None,
            "address": address
        }


    def decode_type_i(self, opcode, instruction):
        rd = (instruction >> 8) & 0b111
        immediate = instruction & 0b11111111 
        
        return {
            "instruction": instruction,
            "opcode": opcode,
            "rd": rd,
            "rs": None,
            "shamt": None,
            "dir": None,
            "immediate": immediate,
            "address": None
        }

    def execute(self, decoded):
        opcode = decoded["opcode"]

        if opcode == OP_PUSH:
            return False
        
        elif opcode == OP_POP:
            return False

        elif opcode == OP_CALL:
            return True

        elif opcode == OP_RET:
            return True

        elif opcode == OP_ADD:
            self.execute_add(decoded)
            return False

        elif opcode == OP_ADDI:
            return False

        elif opcode == OP_SUB:
            self.execute_sub(decoded)
            return False

        elif opcode == OP_LOAD:
            self.execute_load(decoded)
            return False

        elif opcode == OP_LDI:
            return False

        elif opcode == OP_STORE:
            self.execute_store(decoded)
            return False

        elif opcode == OP_STI:
            return False


    def execute_shift(self, decoded):
        rd = decoded["rd"]
        rs = decoded["rs"]
        shamt = decoded["shamt"]
        dir = decoded["dir"]


    def apply_shift(self, value, shamt, direction):
        if direction: # right
            self.set_flag(PSR_C, (value >> (shamt - 1)) & 1) # get last shifted out bit
            return (value >> shamt) & REG_MASK

        else: # left
            self.set_flag(PSR_C, (value >> (8 - shamt)) & 1) # get last shifted out bit
            return (value << shamt) & REG_MASK 


    def execute_store(self, decoded):
        rd = decoded["rd"]
        rs = decoded["rs"]
        shamt = decoded["shamt"]
        dir = decoded["dir"]

        if shamt:
            address = self.apply_shift(self.regs[rd], shamt, dir)
        else:
            address = self.regs[rd]

        self.ram[address] = self.regs[rs]


    def execute_load(self, decoded):
        rd = decoded["rd"]
        rs = decoded["rs"]
        shamt = decoded["shamt"]
        dir = decoded["dir"]

        if shamt:
            address = self.apply_shift(self.regs[rs], shamt, dir)
        else:
            address = self.regs[rs]

        self.regs[rd] = self.ram[address]


    def execute_sub(self, decoded):
        rd = decoded["rd"]
        rs = decoded["rs"]
        shamt = decoded["shamt"]
        dir = decoded["dir"]

        full_sub = self.regs[rd] - self.regs[rs]
        result = full_sub & REG_MASK

        self.set_flag(PSR_C, full_sub < 0x00)

        if shamt:
            result = self.apply_shift(result, shamt, dir)

        self.set_flag(PSR_Z, result == 0)
        self.regs[rd] = result


    def execute_add(self, decoded):
        rd = decoded["rd"]
        rs = decoded["rs"]
        shamt = decoded["shamt"]
        dir = decoded["dir"]

        full_sum = self.regs[rd] + self.regs[rs]
        result = full_sum & REG_MASK # keep lower 8 bytes

        self.set_flag(PSR_C, full_sum > 0xFF)

        if shamt:
            result = self.apply_shift(result, shamt, dir)

        self.set_flag(PSR_Z, result == 0)
        self.regs[rd] = result


    def step(self):
        if self.halted:
            return

        instruction = self.fetch()
        decoded = self.decode(instruction)

        if decoded is None:
            return

        pc_handled = self.execute(decoded)

        if not pc_handled:
            self.pc = (self.pc + 1) & PC_MASK


def main():
    pass

if __name__ == "__main__":
    main()
