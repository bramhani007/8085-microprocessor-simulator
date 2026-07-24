from backend.app.core.cpu8085 import CPU8085


def test_cpu_initialization():
    cpu = CPU8085()

    assert cpu.registers.A == 0x00
    assert cpu.registers.B == 0x00
    assert cpu.registers.PC == 0x0000
    assert cpu.registers.SP == 0xFFFF


def test_register_value_is_8_bit():
    cpu = CPU8085()

    cpu.registers.set_register("A", 0x123)

    assert cpu.registers.A == 0x23


def test_memory_write_and_read():
    cpu = CPU8085()

    cpu.memory.write(0x2000, 0x3E)

    assert cpu.memory.read(0x2000) == 0x3E


def test_register_pairs():
    cpu = CPU8085()
    cpu.registers.set_register_pair("BC", 0x1234)
    assert cpu.registers.B == 0x12
    assert cpu.registers.C == 0x34
    assert cpu.registers.get_register_pair("BC") == 0x1234

    cpu.registers.set_register_pair("HL", 0xABCD)
    assert cpu.registers.H == 0xAB
    assert cpu.registers.L == 0xCD
    assert cpu.registers.get_register_pair("HL") == 0xABCD


def test_psw_operations():
    cpu = CPU8085()
    # A = 0xAA, Flags: S=1, Z=0, AC=1, P=0, CY=1
    cpu.registers.set_register("A", 0xAA)
    cpu.flags.S = 1
    cpu.flags.Z = 0
    cpu.flags.AC = 1
    cpu.flags.P = 0
    cpu.flags.CY = 1

    psw = cpu.get_psw()
    # A: 0xAA (bits 15-8), flags byte (bits 7-0):
    # (1 << 7) | (0 << 6) | (0 << 5) | (1 << 4) | (0 << 3) | (0 << 2) | (1 << 1) | (1 << 0)
    # = 0x80 | 0x10 | 0x02 | 0x01 = 0x93
    # PSW = 0xAA93
    assert psw == 0xAA93

    cpu.reset()
    cpu.set_psw(0x5593)
    assert cpu.registers.A == 0x55
    assert cpu.flags.S == 1
    assert cpu.flags.Z == 0
    assert cpu.flags.AC == 1
    assert cpu.flags.P == 0
    assert cpu.flags.CY == 1


def test_alu_subtraction_ac():
    cpu = CPU8085()
    # Subtracting 0x01 from 0x10: 0x10 - 0x01 = 0x0F
    # Lower nibble: 0x0 - 0x1 = negative, which should set AC (auxiliary carry borrow)
    res, cy, ac = cpu.alu.subtract(0x10, 0x01)
    assert res == 0x0F
    assert cy == 0
    assert ac == 1

    # Subtracting 0x01 from 0x11: 0x11 - 0x01 = 0x10
    # Lower nibble: 0x1 - 0x1 = 0, no borrow, AC should be 0
    res, cy, ac = cpu.alu.subtract(0x11, 0x01)
    assert res == 0x10
    assert cy == 0
    assert ac == 0


def test_alu_logical_operations():
    cpu = CPU8085()
    # AND: 0xF0 & 0x0F = 0x00. CY=0, AC=1
    res, cy, ac = cpu.alu.logical_and(0xF0, 0x0F)
    assert res == 0x00
    assert cy == 0
    assert ac == 1

    # OR: 0xF0 | 0x0F = 0xFF. CY=0, AC=0
    res, cy, ac = cpu.alu.logical_or(0xF0, 0x0F)
    assert res == 0xFF
    assert cy == 0
    assert ac == 0

    # XOR: 0xFF ^ 0x0F = 0xF0. CY=0, AC=0
    res, cy, ac = cpu.alu.logical_xor(0xFF, 0x0F)
    assert res == 0xF0
    assert cy == 0
    assert ac == 0


def test_alu_daa():
    cpu = CPU8085()
    # Accumulator = 0x9B, CY=0, AC=0
    # Lower nibble (0xB) > 9 => add 0x06 => 0x9B + 0x06 = 0xA1 (AC becomes 1)
    # Upper nibble (0xA) > 9 => add 0x60 => 0xA1 + 0x60 = 0x101 (res=0x01, CY becomes 1)
    res, cy, ac = cpu.alu.daa(0x9B, 0, 0)
    assert res == 0x01
    assert cy == 1
    assert ac == 1