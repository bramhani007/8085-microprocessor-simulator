from backend.app.core.cpu8085 import CPU8085


def test_mov_a_b():

    cpu = CPU8085()

    # MVI B, 05H

    cpu.memory.write(0x0000, 0x06)

    cpu.memory.write(0x0001, 0x05)

    # MOV A, B

    cpu.memory.write(0x0002, 0x78)

    # HLT

    cpu.memory.write(0x0003, 0x76)

    # Execute MVI B, 05H

    cpu.step()

    assert cpu.registers.B == 0x05

    # Execute MOV A, B

    cpu.step()

    assert cpu.registers.A == 0x05


def test_mov_c_a():

    cpu = CPU8085()

    # MVI A, 0AH

    cpu.memory.write(0x0000, 0x3E)

    cpu.memory.write(0x0001, 0x0A)

    # MOV C, A

    cpu.memory.write(0x0002, 0x4F)

    # Execute MVI A, 0AH

    cpu.step()

    assert cpu.registers.A == 0x0A

    # Execute MOV C, A

    cpu.step()

    assert cpu.registers.C == 0x0A