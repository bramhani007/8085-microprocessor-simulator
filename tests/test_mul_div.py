from backend.app.core.cpu8085 import CPU8085


def test_mul_b():

    cpu = CPU8085()

    cpu.registers.A = 5
    cpu.registers.B = 3

    cpu.memory.write(0, 0xE8)

    result = cpu.step()

    assert cpu.registers.A == 15
    assert result["instruction"] == "MUL B"


def test_div_b():

    cpu = CPU8085()

    cpu.registers.A = 10
    cpu.registers.B = 2

    cpu.memory.write(0, 0xE9)

    result = cpu.step()

    assert cpu.registers.A == 5
    assert result["instruction"] == "DIV B"


def test_division_by_zero():

    cpu = CPU8085()

    cpu.registers.A = 10
    cpu.registers.B = 0

    cpu.memory.write(0, 0xE9)

    try:

        cpu.step()

        assert False

    except ZeroDivisionError:

        assert True