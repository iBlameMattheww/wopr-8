from model.wopr8_cpu import *


def encode_instruction_r(opcode, rd, rs, shamt = 0, dir = 0):
    instruction = (opcode << 11) & 0xFFFF # keep lower 16 bits
    instruction |= rd << 8
    instruction |= rs << 5
    instruction |= shamt << 2
    instruction |= dir << 1

    return instruction


def test_add_step():
    cpu = WOPR_8()

    cpu.regs[1] = 5
    cpu.regs[2] = 7

    cpu.rom[0] = encode_instruction_r(OP_ADD, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 12
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0


def test_add_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 5
    cpu.regs[2] = -5

    cpu.rom[0] = encode_instruction_r(OP_ADD, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.get_flag(PSR_C) == 0


def test_add_raises_carry():
    cpu = WOPR_8()

    cpu.regs[1] = 100
    cpu.regs[2] = 200

    cpu.rom[0] = encode_instruction_r(OP_ADD, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 44
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 1


def test_add_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 4
    cpu.regs[2] = 5

    cpu.rom[0] = encode_instruction_r(OP_ADD, rd = 1, rs = 2, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 36
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0
    
    cpu.regs[2] = 0 # poor man's shift immediate

    cpu.rom[1] = encode_instruction_r(OP_ADD, rd = 1, rs = 2, shamt = 2, dir = 1)

    cpu.step()

    assert cpu.regs[1] == 9
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0

    cpu.rom[2] = encode_instruction_r(OP_ADD, rd = 1, rs = 2, shamt = 5, dir  = 0)

    cpu.step()

    assert cpu.regs[1] == 32
    assert cpu.pc == 3
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 1
