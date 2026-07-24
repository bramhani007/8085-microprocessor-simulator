from backend.app.core.cpu8085 import CPU8085


def test_mvi_a_execution():

    cpu = CPU8085()

    # Machine code:
    #
    # 3E = MVI A
    # 05 = Data
    #

    program = [

        0x3E,

        0x05

    ]

    # Load program at 2000H

    cpu.memory.load_program(

        program,

        0x2000

    )

    # Set program counter

    cpu.registers.PC = 0x2000

    # Execute instruction

    result = cpu.step()

    # Verify result

    assert cpu.registers.A == 0x05

    assert cpu.registers.PC == 0x2002

    assert result["instruction"] == "MVI A"


def test_mvi_b_execution():

    cpu = CPU8085()

    program = [

        0x06,

        0x03

    ]

    cpu.memory.load_program(

        program,

        0x2000

    )

    cpu.registers.PC = 0x2000

    cpu.step()

    assert cpu.registers.B == 0x03

    assert cpu.registers.PC == 0x2002


def test_add_b_execution():

    cpu = CPU8085()

    # Program:
    #
    # MVI A, 05H
    # MVI B, 03H
    # ADD B
    #

    program = [

        0x3E,

        0x05,

        0x06,

        0x03,

        0x80

    ]

    cpu.memory.load_program(

        program,

        0x2000

    )

    cpu.registers.PC = 0x2000

    # MVI A, 05H

    cpu.step()

    # MVI B, 03H

    cpu.step()

    # ADD B

    cpu.step()

    # Verify result

    assert cpu.registers.A == 0x08

    assert cpu.registers.B == 0x03

    assert cpu.registers.PC == 0x2005


def test_hlt_execution():

    cpu = CPU8085()

    program = [

        0x76

    ]

    cpu.memory.load_program(

        program,

        0x2000

    )

    cpu.registers.PC = 0x2000

    result = cpu.step()

    assert cpu.halted is True

    assert result["instruction"] == "HLT"

    assert cpu.registers.PC == 0x2001


def test_complete_program_execution():

    cpu = CPU8085()

    # Complete program:
    #
    # MVI A, 05H
    # MVI B, 03H
    # ADD B
    # HLT
    #

    program = [

        0x3E,

        0x05,

        0x06,

        0x03,

        0x80,

        0x76

    ]

    cpu.memory.load_program(

        program,

        0x2000

    )

    cpu.registers.PC = 0x2000

    # Execute MVI A

    cpu.step()

    # Execute MVI B

    cpu.step()

    # Execute ADD B

    cpu.step()

    # Execute HLT

    cpu.step()

    # Final verification

    assert cpu.registers.A == 0x08

    assert cpu.registers.B == 0x03

    assert cpu.halted is True

    assert cpu.registers.PC == 0x2006