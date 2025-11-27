import struct
import csv
import sys

# Описание команд
COMMANDS = {
    "LOAD": 0x14,  # Загрузка константы
    "READ": 0xFB,  # Чтение из памяти
    "WRITE": 0x98,  # Запись в память
    "SGN": 0x6B,    # Унарная операция sgn()
}

import csv
import struct

def assemble(input_path, output_path, test_mode):
    with open(input_path, "r") as source, open(output_path, "wb") as binary, open("log.csv", "w", newline='') as log:
        # Создаем CSV writer
        csv_writer = csv.writer(log)
        # Записываем заголовки столбцов
        csv_writer.writerow(["command", "constant", "opcode"])
        
        for line in source:
            parts = line.strip().split()
            if not parts:  # Пропускаем пустые строки
                continue
                
            cmd = parts[0]
            if cmd == "LOAD":
                opcode = COMMANDS[cmd]
                const = int(parts[1])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<I", const))
                
                # Записываем в CSV
                csv_writer.writerow([cmd, const, opcode])
                # Выводим в консоль только при test_mode=1
                if test_mode == 1:
                    print(f"command: {cmd}, constant: {const} - {hex(const)}, opcode: {opcode} - {hex(opcode)}")
                
            elif cmd == "READ":
                opcode = COMMANDS[cmd]
                addr = int(parts[1])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<I", addr))
                
                csv_writer.writerow([cmd, addr, opcode])
                # Выводим в консоль только при test_mode=1
                if test_mode == 1:
                    print(f"command: {cmd}, constant: {addr} - {hex(addr)}, opcode: {opcode} - {hex(opcode)}")
                
            elif cmd == "WRITE":
                opcode = COMMANDS[cmd]
                addr = int(parts[1])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<I", addr))
                
                csv_writer.writerow([cmd, addr, opcode])
                # Выводим в консоль только при test_mode=1
                if test_mode == 1:
                    print(f"command: {cmd}, constant: {addr} - {hex(addr)}, opcode: {opcode} - {hex(opcode)}")
                
            elif cmd == "SGN":
                opcode = COMMANDS[cmd]
                addr = int(parts[1])
                binary.write(struct.pack("B", opcode))
                binary.write(struct.pack("<I", addr))
                csv_writer.writerow([cmd, addr, opcode])
                # Выводим в консоль только при test_mode=1
                if test_mode == 1:
                    print(f"command: {cmd}, constant: {addr} - {hex(addr)}, opcode: {opcode} - {hex(opcode)}")
                
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 assembler.py <input_path> <output_path> test_mode")
        sys.exit(1)
    assemble(sys.argv[1], sys.argv[2], int(sys.argv[3]))