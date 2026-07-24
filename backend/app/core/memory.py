class Memory8085:
    SIZE = 65536

    def __init__(self):
        self.memory = [0x00] * self.SIZE

    def reset(self):
        self.memory = [0x00] * self.SIZE

    def read(self, address):
        if not 0 <= address < self.SIZE:
            raise ValueError("Invalid memory address")

        return self.memory[address]

    def write(self, address, value):
        if not 0 <= address < self.SIZE:
            raise ValueError("Invalid memory address")

        self.memory[address] = value & 0xFF

    def load_program(self, program, start_address=0x0000):
        for index, byte in enumerate(program):
            self.write(start_address + index, byte)

    def dump(self, start, end):
        if not (0 <= start < self.SIZE) or not (0 <= end < self.SIZE):
            raise ValueError("Invalid address range")
        if start > end:
            raise ValueError("Start address cannot be greater than end address")
        return {
            f"{address:04X}": f"{self.memory[address]:02X}"
            for address in range(start, end + 1)
        }