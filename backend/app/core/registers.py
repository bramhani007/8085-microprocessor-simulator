class Registers8085:
    def __init__(self):
        self.A = 0x00
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00

        self.PC = 0x0000
        self.SP = 0xFFFF
        self.IR = 0x00

    def reset(self):
        self.A = 0x00
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00

        self.PC = 0x0000
        self.SP = 0xFFFF
        self.IR = 0x00

    def get_register(self, name):
        name = name.upper()
        if name in ["A", "B", "C", "D", "E", "H", "L", "PC", "SP", "IR"]:
            return getattr(self, name)
        raise ValueError(f"Unknown register: {name}")

    def set_register(self, name, value):
        name = name.upper()

        if name in ["A", "B", "C", "D", "E", "H", "L"]:
            setattr(self, name, value & 0xFF)

        elif name == "PC":
            self.PC = value & 0xFFFF

        elif name == "SP":
            self.SP = value & 0xFFFF

        elif name == "IR":
            self.IR = value & 0xFF

        else:
            raise ValueError(f"Unknown register: {name}")

    def get_register_pair(self, name):
        name = name.upper()
        if name == "BC":
            return (self.B << 8) | self.C
        elif name == "DE":
            return (self.D << 8) | self.E
        elif name == "HL":
            return (self.H << 8) | self.L
        elif name == "SP":
            return self.SP
        elif name == "PC":
            return self.PC
        else:
            raise ValueError(f"Unknown register pair: {name}")

    def set_register_pair(self, name, value):
        name = name.upper()
        value = value & 0xFFFF
        high = (value >> 8) & 0xFF
        low = value & 0xFF

        if name == "BC":
            self.B = high
            self.C = low
        elif name == "DE":
            self.D = high
            self.E = low
        elif name == "HL":
            self.H = high
            self.L = low
        elif name == "SP":
            self.SP = value
        elif name == "PC":
            self.PC = value
        else:
            raise ValueError(f"Unknown register pair: {name}")

    def get_state(self):
        return {
            "A": f"{self.A:02X}",
            "B": f"{self.B:02X}",
            "C": f"{self.C:02X}",
            "D": f"{self.D:02X}",
            "E": f"{self.E:02X}",
            "H": f"{self.H:02X}",
            "L": f"{self.L:02X}",
            "PC": f"{self.PC:04X}",
            "SP": f"{self.SP:04X}",
            "IR": f"{self.IR:02X}"
        }