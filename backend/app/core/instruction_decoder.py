class InstructionDecoder8085:

    def __init__(self):

        # =====================================================
        # REGISTER CODES
        # =====================================================

        self.register_codes = {
            0b000: "B",
            0b001: "C",
            0b010: "D",
            0b011: "E",
            0b100: "H",
            0b101: "L",
            0b111: "A"
        }

        # =====================================================
        # INSTRUCTION MAP
        # =====================================================

        self.instruction_map = {

            # =================================================
            # NOP
            # =================================================

            0x00: {
                "mnemonic": "NOP",
                "size": 1,
                "cycles": 4
            },

            # =================================================
            # MVI
            # =================================================

            0x3E: {
                "mnemonic": "MVI A",
                "size": 2,
                "cycles": 7
            },

            0x06: {
                "mnemonic": "MVI B",
                "size": 2,
                "cycles": 7
            },

            0x0E: {
                "mnemonic": "MVI C",
                "size": 2,
                "cycles": 7
            },

            0x16: {
                "mnemonic": "MVI D",
                "size": 2,
                "cycles": 7
            },

            0x1E: {
                "mnemonic": "MVI E",
                "size": 2,
                "cycles": 7
            },

            0x26: {
                "mnemonic": "MVI H",
                "size": 2,
                "cycles": 7
            },

            0x2E: {
                "mnemonic": "MVI L",
                "size": 2,
                "cycles": 7
            },

            # =================================================
            # ADD REGISTER
            # =================================================

            0x80: {
                "mnemonic": "ADD B",
                "size": 1,
                "cycles": 4
            },

            0x81: {
                "mnemonic": "ADD C",
                "size": 1,
                "cycles": 4
            },

            0x82: {
                "mnemonic": "ADD D",
                "size": 1,
                "cycles": 4
            },

            0x83: {
                "mnemonic": "ADD E",
                "size": 1,
                "cycles": 4
            },

            0x84: {
                "mnemonic": "ADD H",
                "size": 1,
                "cycles": 4
            },

            0x85: {
                "mnemonic": "ADD L",
                "size": 1,
                "cycles": 4
            },

            0x87: {
                "mnemonic": "ADD A",
                "size": 1,
                "cycles": 4
            },

            # =================================================
            # SUB REGISTER
            # =================================================

            0x90: {
                "mnemonic": "SUB B",
                "size": 1,
                "cycles": 4
            },

            0x91: {
                "mnemonic": "SUB C",
                "size": 1,
                "cycles": 4
            },

            0x92: {
                "mnemonic": "SUB D",
                "size": 1,
                "cycles": 4
            },

            0x93: {
                "mnemonic": "SUB E",
                "size": 1,
                "cycles": 4
            },

            0x94: {
                "mnemonic": "SUB H",
                "size": 1,
                "cycles": 4
            },

            0x95: {
                "mnemonic": "SUB L",
                "size": 1,
                "cycles": 4
            },

            0x97: {
                "mnemonic": "SUB A",
                "size": 1,
                "cycles": 4
            },

            # =================================================
            # INR
            # =================================================

            0x3C: {
                "mnemonic": "INR A",
                "size": 1,
                "cycles": 5
            },

            0x04: {
                "mnemonic": "INR B",
                "size": 1,
                "cycles": 5
            },

            0x0C: {
                "mnemonic": "INR C",
                "size": 1,
                "cycles": 5
            },

            0x14: {
                "mnemonic": "INR D",
                "size": 1,
                "cycles": 5
            },

            0x1C: {
                "mnemonic": "INR E",
                "size": 1,
                "cycles": 5
            },

            0x24: {
                "mnemonic": "INR H",
                "size": 1,
                "cycles": 5
            },

            0x2C: {
                "mnemonic": "INR L",
                "size": 1,
                "cycles": 5
            },

            # =================================================
            # DCR
            # =================================================

            0x3D: {
                "mnemonic": "DCR A",
                "size": 1,
                "cycles": 5
            },

            0x05: {
                "mnemonic": "DCR B",
                "size": 1,
                "cycles": 5
            },

            0x0D: {
                "mnemonic": "DCR C",
                "size": 1,
                "cycles": 5
            },

            0x15: {
                "mnemonic": "DCR D",
                "size": 1,
                "cycles": 5
            },

            0x1D: {
                "mnemonic": "DCR E",
                "size": 1,
                "cycles": 5
            },

            0x25: {
                "mnemonic": "DCR H",
                "size": 1,
                "cycles": 5
            },

            0x2D: {
                "mnemonic": "DCR L",
                "size": 1,
                "cycles": 5
            },

            # =================================================
            # JUMP INSTRUCTIONS
            # =================================================

            0xC3: {
                "mnemonic": "JMP",
                "size": 3,
                "cycles": 10
            },

            0xC2: {
                "mnemonic": "JNZ",
                "size": 3,
                "cycles": 10
            },

            0xDA: {
                "mnemonic": "JC",
                "size": 3,
                "cycles": 10
            },

            0xD2: {
                "mnemonic": "JNC",
                "size": 3,
                "cycles": 10
            },

            # =================================================
            # MUL - SIMULATOR EXTENSION
            # =================================================

            0xE8: {
                "mnemonic": "MUL B",
                "size": 1,
                "cycles": 4
            },

            # =================================================
            # DIV - SIMULATOR EXTENSION
            # =================================================

            0xE9: {
                "mnemonic": "DIV B",
                "size": 1,
                "cycles": 4
            },

            # =================================================
            # HLT
            # =================================================

            0x76: {
                "mnemonic": "HLT",
                "size": 1,
                "cycles": 7
            }
        }

    # =====================================================
    # MOV DECODER
    # =====================================================

    def decode_mov(self, opcode):

        """
        MOV instruction format:

        01 DDD SSS

        DDD = Destination Register
        SSS = Source Register

        Register code 110 = M (memory reference).

        Currently only register-to-register MOV
        instructions are supported.
        """

        destination_code = (opcode >> 3) & 0b111

        source_code = opcode & 0b111

        # Reject memory reference M for now

        if (
            destination_code not in self.register_codes
            or source_code not in self.register_codes
        ):
            return None

        destination = self.register_codes[destination_code]

        source = self.register_codes[source_code]

        return {
            "mnemonic": f"MOV {destination}, {source}",
            "size": 1,
            "cycles": 5,
            "destination": destination,
            "source": source
        }

    # =====================================================
    # MAIN DECODER
    # =====================================================

    def decode(self, opcode):

        """
        Decode an 8-bit opcode.

        Returns instruction metadata.
        """

        # Ensure valid 8-bit value

        opcode &= 0xFF

        # =================================================
        # MOV RANGE
        # =================================================

        if (
            0x40 <= opcode <= 0x7F
            and opcode != 0x76
        ):

            mov_instruction = self.decode_mov(opcode)

            if mov_instruction is not None:

                return mov_instruction

        # =================================================
        # NORMAL INSTRUCTION MAP
        # =================================================

        if opcode not in self.instruction_map:

            raise ValueError(
                f"Unknown opcode: {opcode:02X}"
            )

        return self.instruction_map[opcode]