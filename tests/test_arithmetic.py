from backend.app.core.cpu8085 import CPU8085


def test_inr_a():

    cpu = CPU8085()

    # MVI A, 05H
    # INR A
    # HLT

    program = [

        0x3E, 0x05,
        0x3C,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    assert cpu.registers.A == 0x05

    cpu.step()

    assert cpu.registers.A == 0x06

    cpu.step()

    assert cpu.halted is True


def test_dcr_a():

    cpu = CPU8085()

    # MVI A, 05H
    # DCR A
    # HLT

    program = [

        0x3E, 0x05,
        0x3D,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    assert cpu.registers.A == 0x05

    cpu.step()

    assert cpu.registers.A == 0x04

    cpu.step()

    assert cpu.halted is True


def test_sub_b():

    cpu = CPU8085()

    # MVI A, 08H
    # MVI B, 03H
    # SUB B
    # HLT

    program = [

        0x3E, 0x08,
        0x06, 0x03,
        0x90,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    cpu.step()

    cpu.step()

    assert cpu.registers.A == 0x05

    cpu.step()

    assert cpu.halted is True


def test_add_d():

    cpu = CPU8085()

    # MVI A, 05H
    # MVI D, 03H
    # ADD D
    # HLT

    program = [

        0x3E, 0x05,
        0x16, 0x03,
        0x82,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    cpu.step()

    cpu.step()

    assert cpu.registers.A == 0x08

    cpu.step()

    assert cpu.halted is True


def test_inr_zero_flag():

    cpu = CPU8085()

    # MVI A, FFH
    # INR A
    # HLT

    program = [

        0x3E, 0xFF,
        0x3C,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    cpu.step()

    assert cpu.registers.A == 0x00

    assert cpu.flags.Z == 1

    assert cpu.flags.S == 0


def test_dcr_zero_flag():

    cpu = CPU8085()

    # MVI A, 01H
    # DCR A
    # HLT

    program = [

        0x3E, 0x01,
        0x3D,
        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    cpu.step()

    assert cpu.registers.A == 0x00

    assert cpu.flags.Z == 1