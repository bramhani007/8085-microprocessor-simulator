from .registers import Registers8085
from .flags import Flags8085
from .memory import Memory8085
from .alu import ALU8085
from .instruction_decoder import InstructionDecoder8085


class CPU8085:

    def __init__(self):

        # =====================================================
        # CPU COMPONENTS
        # =====================================================

        self.registers = Registers8085()

        self.flags = Flags8085()

        self.memory = Memory8085()

        self.alu = ALU8085()

        self.decoder = InstructionDecoder8085()

        # =====================================================
        # CPU STATE
        # =====================================================

        self.halted = False

        self.cycles = 0

    # =====================================================
    # RESET CPU
    # =====================================================

    def reset(self):

        self.registers.reset()

        self.flags.reset()

        self.memory.reset()

        self.halted = False

        self.cycles = 0

    # =====================================================
    # GET COMPLETE CPU STATE
    # =====================================================

    def get_state(self):

        return {

            "registers": self.registers.get_state(),

            "flags": self.flags.get_state(),

            "halted": self.halted,

            "cycles": self.cycles

        }

    # =====================================================
    # GET PROGRAM STATUS WORD
    # =====================================================

    def get_psw(self):

        """
        8085 PSW FORMAT

        Bits 15-8 : Accumulator

        Bits 7-0  : Flag Register

        Bit 7 : S
        Bit 6 : Z
        Bit 5 : Unused
        Bit 4 : AC
        Bit 3 : Unused
        Bit 2 : P
        Bit 1 : Always 1
        Bit 0 : CY
        """

        flags = 0

        # Sign Flag - Bit 7

        flags |= (

            (self.flags.S & 1)

            << 7

        )

        # Zero Flag - Bit 6

        flags |= (

            (self.flags.Z & 1)

            << 6

        )

        # Auxiliary Carry - Bit 4

        flags |= (

            (self.flags.AC & 1)

            << 4

        )

        # Parity - Bit 2

        flags |= (

            (self.flags.P & 1)

            << 2

        )

        # Bit 1 is always 1

        flags |= 0x02

        # Carry - Bit 0

        flags |= (

            self.flags.CY & 1

        )

        # Combine Accumulator and Flags

        return (

            (

                self.registers.A & 0xFF

            )

            << 8

        ) | flags

    # =====================================================
    # SET PROGRAM STATUS WORD
    # =====================================================

    def set_psw(self, psw):

        """

        Restore Accumulator and Flags
        from a 16-bit PSW value.
        """

        # Ensure 16-bit value

        psw &= 0xFFFF

        # Restore Accumulator

        self.registers.A = (

            (psw >> 8)

            & 0xFF

        )

        # Extract Flag Register

        flags = psw & 0xFF

        # Sign Flag

        self.flags.S = (

            (flags >> 7)

            & 1

        )

        # Zero Flag

        self.flags.Z = (

            (flags >> 6)

            & 1

        )

        # Auxiliary Carry

        self.flags.AC = (

            (flags >> 4)

            & 1

        )

        # Parity

        self.flags.P = (

            (flags >> 2)

            & 1

        )

        # Carry

        self.flags.CY = flags & 1

    # =====================================================
    # FETCH CYCLE
    # =====================================================

    def fetch(self):

        """

        Fetch opcode from memory.

        IR ← Memory[PC]

        """

        # Get Program Counter

        pc = self.registers.PC

        # Read opcode from memory

        opcode = self.memory.read(pc)

        # Store opcode in Instruction Register

        self.registers.IR = opcode

        return opcode

    # =====================================================
    # MVI EXECUTION
    # =====================================================

    def execute_mvi(self, register):

        """

        MVI register, data

        Example:

        MVI A, 05H

        Machine Code:

        3E 05
        """

        # Immediate data is stored
        # at the next memory address

        data = self.memory.read(

            self.registers.PC + 1

        )

        # Store data in register

        self.registers.set_register(

            register,

            data

        )

        # MVI size = 2 bytes

        self.registers.PC += 2

    # =====================================================
    # MOV EXECUTION
    # =====================================================

    def execute_mov(

        self,

        destination,

        source

    ):

        """

        MOV destination, source

        Example:

        MOV A, B

        Operation:

        A ← B

        MOV does not modify flags.

        Size = 1 byte

        """

        # Read source register

        value = (

            self.registers.get_register(

                source

            )

        )

        # Write to destination register

        self.registers.set_register(

            destination,

            value

        )

        # MOV size = 1 byte

        self.registers.PC += 1

    # =====================================================
    # ADD REGISTER EXECUTION
    # =====================================================

    def execute_add_register(self, register):

        """

        ADD register

        Operation:

        A ← A + register

        """

        # Read source register

        value = (

            self.registers.get_register(

                register

            )

        )

        # Perform ALU addition

        result, carry, auxiliary_carry = (

            self.alu.add(

                self.registers.A,

                value

            )

        )

        # Store result in Accumulator

        self.registers.A = result

        # Update Carry Flag

        self.flags.CY = carry

        # Update Auxiliary Carry Flag

        self.flags.AC = auxiliary_carry

        # Update Zero Flag

        self.flags.update_zero(result)

        # Update Sign Flag

        self.flags.update_sign(result)

        # Update Parity Flag

        self.flags.update_parity(result)

        # ADD size = 1 byte

        self.registers.PC += 1

    # =====================================================
    # HLT EXECUTION
    # =====================================================

    def execute_hlt(self):

        """

        Halt CPU execution.

        """

        self.halted = True

        # HLT size = 1 byte

        self.registers.PC += 1

    # =====================================================
    # SINGLE INSTRUCTION EXECUTION
    # =====================================================

    def step(self):

        """

        Execute exactly one instruction.

        Pipeline:

        FETCH
          ↓
        DECODE
          ↓
        EXECUTE
          ↓
        UPDATE STATE

        """

        # =================================================
        # CHECK HALTED STATE
        # =================================================

        if self.halted:

            return {

                "status": "HALTED"

            }

        # =================================================
        # FETCH
        # =================================================

        opcode = self.fetch()

        # =================================================
        # DECODE
        # =================================================

        instruction = (

            self.decoder.decode(

                opcode

            )

        )

        # =================================================
        # EXECUTE
        # =================================================

        # -------------------------------------------------
        # MOV INSTRUCTIONS
        # -------------------------------------------------

        if (

            0x40 <= opcode <= 0x7F

            and opcode != 0x76

        ):

            self.execute_mov(

                instruction[

                    "destination"

                ],

                instruction[

                    "source"

                ]

            )

        # -------------------------------------------------
        # MVI A
        # -------------------------------------------------

        elif opcode == 0x3E:

            self.execute_mvi("A")

        # -------------------------------------------------
        # MVI B
        # -------------------------------------------------

        elif opcode == 0x06:

            self.execute_mvi("B")

        # -------------------------------------------------
        # MVI C
        # -------------------------------------------------

        elif opcode == 0x0E:

            self.execute_mvi("C")

        # -------------------------------------------------
        # MVI D
        # -------------------------------------------------

        elif opcode == 0x16:

            self.execute_mvi("D")

        # -------------------------------------------------
        # MVI E
        # -------------------------------------------------

        elif opcode == 0x1E:

            self.execute_mvi("E")

        # -------------------------------------------------
        # MVI H
        # -------------------------------------------------

        elif opcode == 0x26:

            self.execute_mvi("H")

        # -------------------------------------------------
        # MVI L
        # -------------------------------------------------

        elif opcode == 0x2E:

            self.execute_mvi("L")

        # -------------------------------------------------
        # ADD B
        # -------------------------------------------------

        elif opcode == 0x80:

            self.execute_add_register("B")

        # -------------------------------------------------
        # ADD C
        # -------------------------------------------------

        elif opcode == 0x81:

            self.execute_add_register("C")

        # -------------------------------------------------
        # HLT
        # -------------------------------------------------

        elif opcode == 0x76:

            self.execute_hlt()

        # -------------------------------------------------
        # UNKNOWN INSTRUCTION
        # -------------------------------------------------

        else:

            raise ValueError(

                f"Instruction not implemented: "

                f"{opcode:02X}"

            )

        # =================================================
        # UPDATE MACHINE CYCLES
        # =================================================

        self.cycles += (

            instruction["cycles"]

        )

        # =================================================
        # RETURN EXECUTION RESULT
        # =================================================

        return {

            "status": "EXECUTED",

            "opcode": f"{opcode:02X}",

            "instruction": (

                instruction["mnemonic"]

            ),

            "state": self.get_state()

        }