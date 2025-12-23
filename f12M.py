import struct
import sys

SECTOR_SIZE = 512
TOTAL_SECTORS = 24576        # 12 MB
SECTORS_PER_CLUSTER = 4
RESERVED_SECTORS = 1
NUM_FATS = 2
ROOT_ENTRIES = 512
SECTORS_PER_FAT = 12
MEDIA_DESCRIPTOR = 0xF0

ROOT_DIR_SECTORS = (ROOT_ENTRIES * 32 + SECTOR_SIZE - 1) // SECTOR_SIZE
DATA_START = RESERVED_SECTORS + NUM_FATS * SECTORS_PER_FAT + ROOT_DIR_SECTORS

def write_sector(f, sector, data):
    f.seek(sector * SECTOR_SIZE)
    f.write(data)

def main(filename):
    with open(filename, "wb+") as f:

        # criar ficheiro com tamanho final
        f.seek(TOTAL_SECTORS * SECTOR_SIZE - 1)
        f.write(b"\x00")

        # ---------------- BOOT SECTOR ----------------
        boot = bytearray(SECTOR_SIZE)

        boot[0:3] = b'\xEB\x3C\x90'
        boot[3:11] = b'FAT12   '

        struct.pack_into("<H", boot, 11, SECTOR_SIZE)
        boot[13] = SECTORS_PER_CLUSTER
        struct.pack_into("<H", boot, 14, RESERVED_SECTORS)
        boot[16] = NUM_FATS
        struct.pack_into("<H", boot, 17, ROOT_ENTRIES)
        struct.pack_into("<H", boot, 19, TOTAL_SECTORS)
        boot[21] = MEDIA_DESCRIPTOR
        struct.pack_into("<H", boot, 22, SECTORS_PER_FAT)

        struct.pack_into("<H", boot, 24, 63)   # fake geometry
        struct.pack_into("<H", boot, 26, 255)

        boot[510:512] = b'\x55\xAA'
        write_sector(f, 0, boot)

        # ---------------- FATs ----------------
        fat = bytearray(SECTOR_SIZE)

        # FAT12 initial entries
        fat[0] = MEDIA_DESCRIPTOR
        fat[1] = 0xFF
        fat[2] = 0xFF

        # FAT #1
        write_sector(f, 1, fat)
        # FAT #2
        write_sector(f, 1 + SECTORS_PER_FAT, fat)

        # ---------------- ROOT DIRECTORY ----------------
        zero = bytes(SECTOR_SIZE)
        root_start = RESERVED_SECTORS + NUM_FATS * SECTORS_PER_FAT

        for i in range(ROOT_DIR_SECTORS):
            write_sector(f, root_start + i, zero)

    print("Imagem FAT12 de 12MB criada com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fat12_12mb.py disk12.img")
    else:
        main(sys.argv[1])
