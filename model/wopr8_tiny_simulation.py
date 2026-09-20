from wopr8_cpu import *


def encode_instruction_r(opcode, rd, rs, shamt = 0, dir = 0):
    instruction = (opcode << 11) & 0xFFFF
    instruction |= rd << 8 
    instruction |= rs << 5
    instruction |= shamt << 2
    instruction |= dir << 1

    return instruction


def encode_instruction_i(opcode, rd, immediate):
    instruction = (opcode << 11) & 0xFFFF
    instruction |= rd << 8
    instruction |= immediate

    return instruction


def encode_instruction_j(opcode, address):
    instruction = (opcode << 11) & 0xFFFF 
    instruction |= address

    return instruction



"""
Count from 0 to 5 in a loop
"""

def simple_loop():
    cpu = WOPR_8()

    cpu.rom[0] = encode_instruction_i(OP_LDI, rd = 0, immediate = 0)     # LDI R0, 0
    cpu.rom[1] = encode_instruction_i(OP_LDI, rd = 1, immediate = 5)     # LDI R1, 5
    cpu.rom[2] = encode_instruction_i(OP_ADDI, rd = 0, immediate = 1)    # ADDI R0, 1
    cpu.rom[3] = encode_instruction_r(OP_SUB, rd = 1, rs = 0)            # SUB R1, R0
    cpu.rom[4] = encode_instruction_j(OP_JNZ, address = 1)               # JNZ 1
    cpu.rom[5] = encode_instruction_r(OP_HALT, rd = 0, rs = 0)           # HALT

    while not cpu.halted:
        cpu.step()

    assert cpu.pc == 5
    assert cpu.regs[0] == 5
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.halted == True 

    print("WOPR-8 simple loop simulation passed!")


def main():
    simple_loop()


if __name__ == "__main__":
    main()
