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


def test_sub_step():
    cpu = WOPR_8()

    cpu.regs[1] = 5
    cpu.regs[2] = 4

    cpu.rom[0] = encode_instruction_r(OP_SUB, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 1
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0


def test_sub_rasies_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 5
    cpu.regs[2] = 5

    cpu.rom[0] = encode_instruction_r(OP_SUB, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.get_flag(PSR_C) == 0


def test_sub_raises_carry():
    cpu = WOPR_8()
    
    cpu.regs[1] = 4
    cpu.regs[2] = 5

    cpu.rom[0] = encode_instruction_r(OP_SUB, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 255 # 11111111 -> -1 in two's complement
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 1


def test_load_step():
    cpu = WOPR_8()

    cpu.ram[0] = 42

    cpu.regs[1] = 0

    cpu.rom[0] = encode_instruction_r(OP_LOAD, rd = 1, rs = 0)

    cpu.step()

    assert cpu.regs[1] == 42
    assert cpu.pc == 1


def test_load_post_shift():
    cpu = WOPR_8()

    cpu.ram[0] = 42

    cpu.regs[1] = 0
    cpu.regs[2] = 1

    cpu.rom[0] = encode_instruction_r(OP_LOAD, rd = 1, rs = 2, shamt = 1, dir = 1)

    cpu.step()

    assert cpu.regs[1] == 42
    assert cpu.pc == 1


def test_store_step():
    cpu = WOPR_8()

    cpu.regs[1] = 42
    cpu.regs[2] = 0

    cpu.rom[0] = encode_instruction_r(OP_STORE, rd = 2, rs = 1)

    cpu.step()

    assert cpu.ram[0] == 42
    assert cpu.pc == 1


def test_store_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 42
    cpu.regs[2] = 1

    cpu.rom[0] = encode_instruction_r(OP_STORE, rd = 2, rs = 1, shamt = 1, dir = 1)

    cpu.step()

    assert cpu.ram[0] == 42
    assert cpu.pc == 1


def test_move_step():
    cpu = WOPR_8()

    cpu.regs[1] = 0
    cpu.regs[2] = 3

    cpu.rom[0] = encode_instruction_r(OP_MOVE, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 3
    assert cpu.pc == 1


def test_move_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 0
    cpu.regs[2] = 1

    cpu.rom[0] = encode_instruction_r(OP_MOVE, rd = 1, rs = 2, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 128
    assert cpu.pc == 1


def test_and_step():
    cpu = WOPR_8()

    cpu.regs[1] = 255
    cpu.regs[2] = 128

    cpu.rom[0] = encode_instruction_r(OP_AND, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 128
    assert cpu.pc == 1


def test_and_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 255
    cpu.regs[2] = 0

    cpu.rom[0] = encode_instruction_r(OP_AND, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1


def test_and_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 1

    cpu.rom[0] = encode_instruction_r(OP_AND, rd = 1, rs = 2, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 4
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0

    cpu.regs[2] = 4

    cpu.rom[1] = encode_instruction_r(OP_AND, rd = 1, rs = 2, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 1


def test_or_step():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 2

    cpu.rom[0] = encode_instruction_r(OP_OR, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 3
    assert cpu.pc == 1


def test_or_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 0
    cpu.regs[2] = 0

    cpu.rom[0] = encode_instruction_r(OP_OR, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1


def test_or_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 2

    cpu.rom[0] = encode_instruction_r(OP_OR, rd = 1, rs = 2, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 12
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0

    cpu.regs[2] = 4

    cpu.rom[1] = encode_instruction_r(OP_OR, rd = 1, rs = 2, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 1


def test_xor_step():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 3

    cpu.rom[0] = encode_instruction_r(OP_XOR, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 2
    assert cpu.pc == 1


def test_xor_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 1

    cpu.rom[0] = encode_instruction_r(OP_XOR, rd = 1, rs = 2)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1


def test_xor_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 3

    cpu.rom[0] = encode_instruction_r(OP_XOR, rd = 1, rs = 2, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 8
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0

    cpu.regs[2] = 8

    cpu.rom[1] = encode_instruction_r(OP_XOR, rd = 1, rs = 2, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 1


def test_not_step():
    cpu = WOPR_8()

    cpu.regs[1] = 0

    cpu.rom[0] = encode_instruction_r(OP_NOT, rd = 1, rs = 0)

    cpu.step()

    assert cpu.regs[1] == 255
    assert cpu.pc == 1


def test_not_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 255

    cpu.rom[0] = encode_instruction_r(OP_NOT, rd = 0, rs = 1)

    cpu.step()

    assert cpu.regs[0] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1


def test_not_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 0

    cpu.rom[0] = encode_instruction_r(OP_NOT, rd = 1, rs = 0, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 252
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0

    cpu.rom[1] = encode_instruction_r(OP_NOT, rd = 1, rs = 0, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 128
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 0


def test_shift_step():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 2

    cpu.rom[0] = encode_instruction_r(OP_SHIFT, rd = 1, rs = 2, shamt = 0, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 4
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0


def test_shift_raises_zero():
    cpu = WOPR_8()

    cpu.regs[1] = 0
    cpu.regs[2] = 8

    cpu.rom[0] = encode_instruction_r(OP_SHIFT, rd = 1, rs = 2, shamt = 0, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.get_flag(PSR_C) == 0


def test_shift_raises_carry():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 8

    cpu.rom[0] = encode_instruction_r(OP_SHIFT, rd = 1, rs = 2, shamt = 0, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.get_flag(PSR_C) == 1


def test_shift_post_shift():
    cpu = WOPR_8()

    cpu.regs[1] = 1
    cpu.regs[2] = 2

    cpu.rom[0] = encode_instruction_r(OP_SHIFT, rd = 1, rs = 2, shamt = 2, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 16
    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 0
    assert cpu.get_flag(PSR_C) == 0

    cpu.rom[1] = encode_instruction_r(OP_SHIFT, rd = 1, rs = 2, shamt = 7, dir = 0)

    cpu.step()

    assert cpu.regs[1] == 0
    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 1
    assert cpu.get_flag(PSR_C) == 0


def test_cmp_step():
    cpu = WOPR_8()

    cpu.regs[1] = 5
    cpu.regs[2] = 5

    cpu.rom[0] = encode_instruction_r(OP_CMP, rd = 1, rs = 2)

    cpu.step()

    assert cpu.pc == 1
    assert cpu.get_flag(PSR_Z) == 1

    cpu.regs[2] = 4

    cpu.rom[1] = encode_instruction_r(OP_CMP, rd = 1, rs = 2)

    cpu.step()

    assert cpu.pc == 2
    assert cpu.get_flag(PSR_Z) == 0


def test_nop_step():
    cpu = WOPR_8()

    cpu.rom[0] = encode_instruction_r(OP_NOP, rd = 0, rs = 0)

    cpu.step()

    assert cpu.pc == 1


def test_halt_step():
    cpu = WOPR_8()

    cpu.rom[0] = encode_instruction_r(OP_HALT, rd = 0, rs = 0)

    cpu.step()

    assert cpu.pc == 1
    assert cpu.halted == True
    assert cpu.get_flag(PSR_HALTED) == 1
