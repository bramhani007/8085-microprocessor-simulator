class Flags8085:
    def __init__(self):
        self.S = 0
        self.Z = 0
        self.AC = 0
        self.P = 0
        self.CY = 0

    def reset(self):
        self.S = 0
        self.Z = 0
        self.AC = 0
        self.P = 0
        self.CY = 0

    def update_zero(self, value):
        self.Z = 1 if (value & 0xFF) == 0 else 0

    def update_sign(self, value):
        self.S = 1 if (value & 0x80) != 0 else 0

    def update_parity(self, value):
        ones = bin(value & 0xFF).count("1")
        self.P = 1 if ones % 2 == 0 else 0

    def get_state(self):
        return {
            "S": self.S,
            "Z": self.Z,
            "AC": self.AC,
            "P": self.P,
            "CY": self.CY
        }

    def get_byte(self):
        return (
            (self.S << 7) |
            (self.Z << 6) |
            (0 << 5) |
            (self.AC << 4) |
            (0 << 3) |
            (self.P << 2) |
            (1 << 1) |
            (self.CY << 0)
        )

    def set_byte(self, byte):
        self.S = (byte >> 7) & 1
        self.Z = (byte >> 6) & 1
        self.AC = (byte >> 4) & 1
        self.P = (byte >> 2) & 1
        self.CY = byte & 1