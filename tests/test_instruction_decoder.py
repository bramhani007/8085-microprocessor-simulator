from backend.app.core.instruction_decoder import (
    InstructionDecoder8085
)


def test_decode_mvi_a():

    decoder = InstructionDecoder8085()

    instruction = decoder.decode(0x3E)

    assert instruction["mnemonic"] == "MVI A"
    assert instruction["size"] == 2
    assert instruction["cycles"] == 7


def test_decode_mvi_b():

    decoder = InstructionDecoder8085()

    instruction = decoder.decode(0x06)

    assert instruction["mnemonic"] == "MVI B"
    assert instruction["size"] == 2
    assert instruction["cycles"] == 7


def test_decode_add_b():

    decoder = InstructionDecoder8085()

    instruction = decoder.decode(0x80)

    assert instruction["mnemonic"] == "ADD B"
    assert instruction["size"] == 1
    assert instruction["cycles"] == 4


def test_decode_hlt():

    decoder = InstructionDecoder8085()

    instruction = decoder.decode(0x76)

    assert instruction["mnemonic"] == "HLT"
    assert instruction["size"] == 1
    assert instruction["cycles"] == 7