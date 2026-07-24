class InstructionDecoder8085:

    def __init__(self):

        self.register_codes = {

            0b000: "B",

            0b001: "C",

            0b010: "D",

            0b011: "E",

            0b100: "H",

            0b101: "L",

            0b111: "A"

        }

        self.instruction_map = {

            # =============================================
            # NOP
            # =============================================

            0x00: {

                "mnemonic": "NOP",

                "size": 1,

                "cycles": 4

            },

            # =============================================
            # MVI
            # =============================================

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

            # =============================================
            # ADD
            # =============================================

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

            # =============================================
            # HLT
            # =============================================

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

        DDD = Destination register

        SSS = Source register

        """

        # Extract destination register

        destination_code = (

            (opcode >> 3) & 0b111

        )

        # Extract source register

        source_code = opcode & 0b111

        # Check if registers are valid

        if (

            destination_code not in self.register_codes

            or source_code not in self.register_codes

        ):

            return None

        destination = (

            self.register_codes[

                destination_code

            ]

        )

        source = (

            self.register_codes[

                source_code

            ]

        )

        return {

            "mnemonic": (

                f"MOV "

                f"{destination}, "

                f"{source}"

            ),

            "size": 1,

            "cycles": 5,

            "destination": destination,

            "source": source

        }

    # =====================================================
    # MAIN DECODER
    # =====================================================

    def decode(self, opcode):

        # =============================================
        # MOV RANGE
        # =============================================

        # MOV instructions have:

        # 01 DDD SSS

        if (

            0x40 <= opcode <= 0x7F

            and opcode != 0x76

        ):

            mov_instruction = (

                self.decode_mov(opcode)

            )

            if mov_instruction is not None:

                return mov_instruction

        # =============================================
        # NORMAL INSTRUCTION MAP
        # =============================================

        if opcode not in self.instruction_map:

            raise ValueError(

                f"Unknown opcode: "

                f"{opcode:02X}"

            )

        return self.instruction_map[opcode]