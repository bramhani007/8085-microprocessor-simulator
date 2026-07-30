from backend.app.core.cpu8085 import CPU8085


def test_multiplication():

    cpu = CPU8085()

    # MVI A, 05H
    cpu.memory.write(0x0000, 0x3E)
    cpu.memory.write(0x0001, 0x05)

    # MVI B, 03H
    cpu.memory.write(0x0002, 0x06)
    cpu.memory.write(0x0003, 0x03)

    # MUL B
    cpu.memory.write(0x0004, 0xE8)

    # HLT
    cpu.memory.write(0x0005, 0x76)

    cpu.step()
    cpu.step()
    cpu.step()

    assert cpu.registers.A == 15


def test_division():

    cpu = CPU8085()

    # MVI A, 15H
    cpu.memory.write(0x0000, 0x3E)
    cpu.memory.write(0x0001, 0x15)

    # MVI B, 03H
    cpu.memory.write(0x0002, 0x06)
    cpu.memory.write(0x0003, 0x03)

    # DIV B
    cpu.memory.write(0x0004, 0xE9)

    # HLT
    cpu.memory.write(0x0005, 0x76)

    cpu.step()
    cpu.step()
    cpu.step()

    assert cpu.registers.A == 7