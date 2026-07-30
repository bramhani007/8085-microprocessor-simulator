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
    # GET CPU STATE
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

        flag_byte = 0

        # Sign Flag - Bit 7
        flag_byte |= (

            (self.flags.S & 1) << 7

        )

        # Zero Flag - Bit 6
        flag_byte |= (

            (self.flags.Z & 1) << 6

        )

        # Auxiliary Carry - Bit 4
        flag_byte |= (

            (self.flags.AC & 1) << 4

        )

        # Parity Flag - Bit 2
        flag_byte |= (

            (self.flags.P & 1) << 2

        )

        # Bit 1 is always 1
        flag_byte |= 0x02

        # Carry Flag - Bit 0
        flag_byte |= (

            self.flags.CY & 1

        )

        # PSW = Accumulator + Flag Register
        return (

            ((self.registers.A & 0xFF) << 8)

            | flag_byte

        )

    # =====================================================
    # SET PROGRAM STATUS WORD
    # =====================================================

    def set_psw(self, psw):

        psw &= 0xFFFF

        # Restore Accumulator
        self.registers.A = (

            (psw >> 8) & 0xFF

        )

        flag_byte = psw & 0xFF

        # Restore Flags
        self.flags.S = (

            (flag_byte >> 7) & 1

        )

        self.flags.Z = (

            (flag_byte >> 6) & 1

        )

        self.flags.AC = (

            (flag_byte >> 4) & 1

        )

        self.flags.P = (

            (flag_byte >> 2) & 1

        )

        self.flags.CY = flag_byte & 1

    # =====================================================
    # FETCH
    # =====================================================

    def fetch(self):

        pc = self.registers.PC

        opcode = self.memory.read(pc)

        self.registers.IR = opcode

        return opcode

    # =====================================================
    # UPDATE COMMON FLAGS
    # =====================================================

    def update_common_flags(self, result):

        result &= 0xFF

        # Sign Flag
        self.flags.S = (

            1 if result & 0x80 else 0

        )

        # Zero Flag
        self.flags.Z = (

            1 if result == 0 else 0

        )

        # Parity Flag
        self.flags.P = (

            1

            if bin(result).count("1") % 2 == 0

            else 0

        )

    # =====================================================
    # MVI
    # =====================================================

    def execute_mvi(self, register):

        data = self.memory.read(

            self.registers.PC + 1

        )

        self.registers.set_register(

            register,

            data

        )

        # MVI does not affect flags
        self.registers.PC += 2

    # =====================================================
    # MOV
    # =====================================================

    def execute_mov(

        self,

        destination,

        source

    ):

        value = self.registers.get_register(

            source

        )

        self.registers.set_register(

            destination,

            value

        )

        # MOV does not affect flags
        self.registers.PC += 1

    # =====================================================
    # ADD REGISTER
    # =====================================================

    def execute_add_register(self, register):

        value = self.registers.get_register(

            register

        )

        result, carry, auxiliary_carry = (

            self.alu.add(

                self.registers.A,

                value

            )

        )

        self.registers.A = result

        self.flags.CY = carry

        self.flags.AC = auxiliary_carry

        self.update_common_flags(result)

        self.registers.PC += 1

    # =====================================================
    # SUB REGISTER
    # =====================================================

    def execute_sub_register(self, register):

        value = self.registers.get_register(

            register

        )

        result, borrow, auxiliary_borrow = (

            self.alu.subtract(

                self.registers.A,

                value

            )

        )

        self.registers.A = result

        # In 8085 subtraction,
        # CY represents borrow

        self.flags.CY = borrow

        self.flags.AC = auxiliary_borrow

        self.update_common_flags(result)

        self.registers.PC += 1

    # =====================================================
    # MUL REGISTER
    # =====================================================

    def execute_mul_register(self, register):

        """

        Custom Simulator Extension

        A ← A × register

        Example:

        A = 05H
        B = 03H

        MUL B

        Result:

        A = 0FH

        """

        value = self.registers.get_register(

            register

        )

        result = (

            self.registers.A * value

        ) & 0xFF

        self.registers.A = result

        # Update S, Z and P
        self.update_common_flags(result)

        # Custom MUL behavior
        self.flags.CY = 0

        self.flags.AC = 0

        self.registers.PC += 1

    # =====================================================
    # DIV REGISTER
    # =====================================================

    def execute_div_register(self, register):

        """

        Custom Simulator Extension

        A ← A ÷ register

        Example:

        A = 0AH
        B = 02H

        DIV B

        Result:

        A = 05H

        """

        value = self.registers.get_register(

            register

        )

        if value == 0:

            raise ZeroDivisionError(

                "Division by zero is not allowed"

            )

        result = (

            self.registers.A // value

        ) & 0xFF

        self.registers.A = result

        # Update S, Z and P
        self.update_common_flags(result)

        # Custom DIV behavior
        self.flags.CY = 0

        self.flags.AC = 0

        self.registers.PC += 1

    # =====================================================
    # INR
    # =====================================================

    def execute_inr(self, register):

        old_value = self.registers.get_register(

            register

        )

        result = (

            (old_value + 1) & 0xFF

        )

        self.registers.set_register(

            register,

            result

        )

        # INR affects S, Z, AC, P
        # INR does NOT affect CY

        self.flags.S = (

            1 if result & 0x80 else 0

        )

        self.flags.Z = (

            1 if result == 0 else 0

        )

        self.flags.P = (

            1

            if bin(result).count("1") % 2 == 0

            else 0

        )

        self.flags.AC = (

            1

            if (old_value & 0x0F) == 0x0F

            else 0

        )

        self.registers.PC += 1

    # =====================================================
    # DCR
    # =====================================================

    def execute_dcr(self, register):

        old_value = self.registers.get_register(

            register

        )

        result = (

            (old_value - 1) & 0xFF

        )

        self.registers.set_register(

            register,

            result

        )

        # DCR affects S, Z, AC, P
        # DCR does NOT affect CY

        self.flags.S = (

            1 if result & 0x80 else 0

        )

        self.flags.Z = (

            1 if result == 0 else 0

        )

        self.flags.P = (

            1

            if bin(result).count("1") % 2 == 0

            else 0

        )

        self.flags.AC = (

            1

            if (old_value & 0x0F) == 0

            else 0

        )

        self.registers.PC += 1

    # =====================================================
    # READ 16-BIT ADDRESS
    # =====================================================

    def read_address(self):

        low_byte = self.memory.read(

            self.registers.PC + 1

        )

        high_byte = self.memory.read(

            self.registers.PC + 2

        )

        return (

            (high_byte << 8)

            | low_byte

        )

    # =====================================================
    # JMP
    # =====================================================

    def execute_jmp(self):

        address = self.read_address()

        self.registers.PC = address

    # =====================================================
    # JNZ
    # =====================================================

    def execute_jnz(self):

        address = self.read_address()

        if self.flags.Z == 0:

            self.registers.PC = address

        else:

            self.registers.PC += 3

    # =====================================================
    # JC
    # =====================================================

    def execute_jc(self):

        address = self.read_address()

        if self.flags.CY == 1:

            self.registers.PC = address

        else:

            self.registers.PC += 3

    # =====================================================
    # JNC
    # =====================================================

    def execute_jnc(self):

        address = self.read_address()

        if self.flags.CY == 0:

            self.registers.PC = address

        else:

            self.registers.PC += 3

    # =====================================================
    # NOP
    # =====================================================

    def execute_nop(self):

        self.registers.PC += 1

    # =====================================================
    # HLT
    # =====================================================

    def execute_hlt(self):

        self.halted = True

        self.registers.PC += 1

    # =====================================================
    # SINGLE INSTRUCTION EXECUTION
    # =====================================================

    def step(self):

        # -------------------------------------------------
        # HALTED CPU
        # -------------------------------------------------

        if self.halted:

            return {

                "status": "HALTED",

                "state": self.get_state()

            }

        # -------------------------------------------------
        # FETCH
        # -------------------------------------------------

        opcode = self.fetch()

        # -------------------------------------------------
        # DECODE
        # -------------------------------------------------

        instruction = self.decoder.decode(

            opcode

        )

        # -------------------------------------------------
        # MOV
        # -------------------------------------------------

        if (

            0x40 <= opcode <= 0x7F

            and opcode != 0x76

        ):

            self.execute_mov(

                instruction["destination"],

                instruction["source"]

            )

        # -------------------------------------------------
        # NOP
        # -------------------------------------------------

        elif opcode == 0x00:

            self.execute_nop()

        # -------------------------------------------------
        # MVI
        # -------------------------------------------------

        elif opcode == 0x3E:

            self.execute_mvi("A")

        elif opcode == 0x06:

            self.execute_mvi("B")

        elif opcode == 0x0E:

            self.execute_mvi("C")

        elif opcode == 0x16:

            self.execute_mvi("D")

        elif opcode == 0x1E:

            self.execute_mvi("E")

        elif opcode == 0x26:

            self.execute_mvi("H")

        elif opcode == 0x2E:

            self.execute_mvi("L")

        # -------------------------------------------------
        # ADD
        # -------------------------------------------------

        elif opcode == 0x80:

            self.execute_add_register("B")

        elif opcode == 0x81:

            self.execute_add_register("C")

        elif opcode == 0x82:

            self.execute_add_register("D")

        elif opcode == 0x83:

            self.execute_add_register("E")

        elif opcode == 0x84:

            self.execute_add_register("H")

        elif opcode == 0x85:

            self.execute_add_register("L")

        # -------------------------------------------------
        # SUB
        # -------------------------------------------------

        elif opcode == 0x90:

            self.execute_sub_register("B")

        elif opcode == 0x91:

            self.execute_sub_register("C")

        elif opcode == 0x92:

            self.execute_sub_register("D")

        elif opcode == 0x93:

            self.execute_sub_register("E")

        elif opcode == 0x94:

            self.execute_sub_register("H")

        elif opcode == 0x95:

            self.execute_sub_register("L")

        # -------------------------------------------------
        # MUL
        # -------------------------------------------------

        elif opcode == 0xE8:

            self.execute_mul_register("B")

        # -------------------------------------------------
        # DIV
        # -------------------------------------------------

        elif opcode == 0xE9:

            self.execute_div_register("B")

        # -------------------------------------------------
        # INR
        # -------------------------------------------------

        elif opcode == 0x3C:

            self.execute_inr("A")

        elif opcode == 0x04:

            self.execute_inr("B")

        elif opcode == 0x0C:

            self.execute_inr("C")

        elif opcode == 0x14:

            self.execute_inr("D")

        elif opcode == 0x1C:

            self.execute_inr("E")

        elif opcode == 0x24:

            self.execute_inr("H")

        elif opcode == 0x2C:

            self.execute_inr("L")

        # -------------------------------------------------
        # DCR
        # -------------------------------------------------

        elif opcode == 0x3D:

            self.execute_dcr("A")

        elif opcode == 0x05:

            self.execute_dcr("B")

        elif opcode == 0x0D:

            self.execute_dcr("C")

        elif opcode == 0x15:

            self.execute_dcr("D")

        elif opcode == 0x1D:

            self.execute_dcr("E")

        elif opcode == 0x25:

            self.execute_dcr("H")

        elif opcode == 0x2D:

            self.execute_dcr("L")

        # -------------------------------------------------
        # JMP
        # -------------------------------------------------

        elif opcode == 0xC3:

            self.execute_jmp()

        # -------------------------------------------------
        # JNZ
        # -------------------------------------------------

        elif opcode == 0xC2:

            self.execute_jnz()

        # -------------------------------------------------
        # JC
        # -------------------------------------------------

        elif opcode == 0xDA:

            self.execute_jc()

        # -------------------------------------------------
        # JNC
        # -------------------------------------------------

        elif opcode == 0xD2:

            self.execute_jnc()

        # -------------------------------------------------
        # HLT
        # -------------------------------------------------

        elif opcode == 0x76:

            self.execute_hlt()

        # -------------------------------------------------
        # UNKNOWN
        # -------------------------------------------------

        else:

            raise ValueError(

                f"Instruction not implemented: "

                f"{opcode:02X}"

            )

        # -------------------------------------------------
        # UPDATE MACHINE CYCLES
        # -------------------------------------------------

        self.cycles += (

            instruction["cycles"]

        )

        # -------------------------------------------------
        # RETURN EXECUTION RESULT
        # -------------------------------------------------

        return {

            "status": "EXECUTED",

            "opcode": f"{opcode:02X}",

            "instruction": (

                instruction["mnemonic"]

            ),

            "state": self.get_state()

        }