from backend.app.core.cpu8085 import CPU8085


def test_jmp():

    cpu = CPU8085()

    program = [

        0xC3,
        0x05,
        0x00,

        0x3E,
        0x99,

        0x3E,
        0x42,

        0x76

    ]

    cpu.memory.load_program(program)

    cpu.step()

    assert cpu.registers.PC == 0x0005

    cpu.step()

    assert cpu.registers.A == 0x42


def test_jnz_taken():

    cpu = CPU8085()

    program = [

        0xC2,
        0x06,
        0x00,

        0x3E,
        0x99,

        0x00,

        0x3E,
        0x42

    ]

    cpu.memory.load_program(program)

    cpu.flags.Z = 0

    cpu.step()

    assert cpu.registers.PC == 0x0006


def test_jnz_not_taken():

    cpu = CPU8085()

    program = [

        0xC2,
        0x06,
        0x00,

        0x3E,
        0x42,

        0x76,

        0x00

    ]

    cpu.memory.load_program(program)

    cpu.flags.Z = 1

    cpu.step()

    assert cpu.registers.PC == 0x0003


def test_jc_taken():

    cpu = CPU8085()

    program = [

        0xDA,
        0x06,
        0x00,

        0x3E,
        0x99,

        0x00,

        0x76

    ]

    cpu.memory.load_program(program)

    cpu.flags.CY = 1

    cpu.step()

    assert cpu.registers.PC == 0x0006


def test_jnc_taken():

    cpu = CPU8085()

    program = [

        0xD2,
        0x06,
        0x00,

        0x3E,
        0x99,

        0x00,

        0x76

    ]

    cpu.memory.load_program(program)

    cpu.flags.CY = 0

    cpu.step()

    assert cpu.registers.PC == 0x0006