import struct
import sys
import csv

MEMORY_SIZE = 1024

class VirtualMachine:
    def __init__(self):
        self.memory = [0] * MEMORY_SIZE
        self.accumulator = 0

    def load(self, const):
        self.accumulator = const
        print("LOAD функция")
        print("аккумулятор: ", self.accumulator)

    def read(self,const):
        print("READ функция")
        print("аккумулятор до чтения: ", self.accumulator)
        self.accumulator = self.memory[const]
        print("аккумулятор после чтения: ", self.accumulator)
        

    def write(self, addr):
        print("WRITE функция")
        print("аккумулятор адрес ")
        print(self.accumulator, "      ", addr)
        self.memory[addr] = self.accumulator

    def sgn(self, addr):
        if self.accumulator > 0:
            self.memory[addr] = 1
        elif self.accumulator < 0:
            self.memory[addr] = -1
        elif self.accumulator == 0:
            self.memory[addr] = 0
        print("SGN функция")
        print("аккумулятор адрес ")
        print(self.accumulator, "      ", addr)

    def execute(self, program_path, result_path, mem_range):
        with open(program_path, "rb") as binary, open(result_path, "w") as result:
            while byte := binary.read(1):
                opcode = struct.unpack("B", byte)[0]
                if opcode == 0x14:  # LOAD
                    const = struct.unpack("<i", binary.read(4))[0]  # Знаковое значение
                    self.load(const)
                elif opcode == 0xFB:  # READ
                    addr = struct.unpack("<I", binary.read(4))[0]
                    self.read(addr)
                elif opcode == 0x98:  # WRITE
                    addr = struct.unpack("<I", binary.read(4))[0]
                    self.write(addr)
                elif opcode == 0x6B:  # sgn
                    addr = struct.unpack("<I", binary.read(4))[0]
                    self.sgn(addr)
            
            start, end = mem_range
            numbers=list(range(start,end))
            result_data = {'number': numbers,'memory': self.memory[start:end]}
            with open(result_path, 'w', newline='', encoding='utf-8') as output:
                writer = csv.writer(output)
                
                # Запись заголовков
                writer.writerow(['number', 'memory'])
                
                # Запись данных построчно
                for i in range(len(numbers)):
                    writer.writerow([numbers[i], result_data['memory'][i]])
            # yaml.dump(result_data, result)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 interpreter.py <binary_path> <result_path> <mem_start> <mem_end>")
        sys.exit(1)

    binary_path = sys.argv[1]
    result_path = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])

    vm = VirtualMachine()
    vm.execute(binary_path, result_path, (mem_start, mem_end))