class ALU8085:

    def add(self, a, b, carry=0):
        result = a + b + carry

        carry_flag = 1 if result > 0xFF else 0

        auxiliary_carry = (
            1 if ((a & 0x0F) + (b & 0x0F) + carry) > 0x0F
            else 0
        )

        return result & 0xFF, carry_flag, auxiliary_carry

    def subtract(self, a, b, borrow=0):
        result = a - b - borrow

        carry_flag = 1 if result < 0 else 0

        # Subtraction AC is set if there is a borrow from bit 4 to bit 3.
        # This is equivalent to low nibble subtraction being negative.
        auxiliary_carry = (
            1 if ((a & 0x0F) - (b & 0x0F) - borrow) < 0
            else 0
        )

        return result & 0xFF, carry_flag, auxiliary_carry

    def logical_and(self, a, b):
        result = a & b
        # In 8085, AND operation sets AC to 1, and clears CY to 0
        return result & 0xFF, 0, 1

    def logical_or(self, a, b):
        result = a | b
        # In 8085, OR operation clears AC to 0, and clears CY to 0
        return result & 0xFF, 0, 0

    def logical_xor(self, a, b):
        result = a ^ b
        # In 8085, XOR operation clears AC to 0, and clears CY to 0
        return result & 0xFF, 0, 0

    def daa(self, a, cy, ac):
        correction = 0
        new_cy = cy

        # Step 1: Lower Nibble correction
        if (a & 0x0F) > 9 or ac == 1:
            correction += 0x06

        # Step 2: Upper Nibble correction
        if (a + (correction & 0x0F)) > 0x9F or cy == 1:
            correction += 0x60
            new_cy = 1

        result = a + correction
        new_ac = 1 if ((a & 0x0F) + (correction & 0x0F)) > 0x0F else 0

        return result & 0xFF, new_cy, new_ac