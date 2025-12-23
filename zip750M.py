import struct
import sys

SECTOR_SIZE = 512
TOTAL_SECTORS = 1_536_000
RESERVED_SECTORS = 32
SECTORS_PER_FAT = 1500
SECTORS_PER_CLUSTER = 32

def write_sector(f, sector, data):
    f.seek(sector * SECTOR_SIZE)
    f.write(data)

def main(filename):
    with open(filename, "wb+") as f:

        # --- criar ficheiro com tamanho final ---
        f.seek(TOTAL_SECTORS * SECTOR_SIZE - 1)
        f.write(b"\x00")

        # ================= BOOT SECTOR =================
        boot = bytearray(SECTOR_SIZE)
        boot[0:3] = b'\xEB\x58\x90'
        boot[3:11] = b'ZIP750  '

        struct.pack_into("<H", boot, 11, SECTOR_SIZE)
        boot[13] = SECTORS_PER_CLUSTER
        struct.pack_into("<H", boot, 14, RESERVED_SECTORS)
        boot[16] = 2                          # FATs
        boot[21] = 0xF8                       # fixed disk

        struct.pack_into("<I", boot, 32, TOTAL_SECTORS)
        struct.pack_into("<I", boot, 36, SECTORS_PER_FAT)

        struct.pack_into("<I", boot, 44, 2)   # root cluster
        struct.pack_into("<H", boot, 48, 1)   # FSInfo sector
        struct.pack_into("<H", boot, 50, 6)   # backup boot

        boot[510:512] = b'\x55\xAA'
        write_sector(f, 0, boot)

        # ================= FSINFO =================
        fsinfo = bytearray(SECTOR_SIZE)
        struct.pack_into("<I", fsinfo, 0,   0x41615252)  # RRaA
        struct.pack_into("<I", fsinfo, 484, 0x61417272)  # rrAa
        struct.pack_into("<I", fsinfo, 488, 0xFFFFFFFF)
        struct.pack_into("<I", fsinfo, 492, 0xFFFFFFFF)
        fsinfo[510:512] = b'\x55\xAA'
        write_sector(f, 1, fsinfo)

        # ================= BACKUP BOOT =================
        write_sector(f, 6, boot)

        # ================= FATs =================
        fat_start = RESERVED_SECTORS
        fat_sector = bytearray(SECTOR_SIZE)

        # FAT32 initial entries
        struct.pack_into("<I", fat_sector, 0, 0x0FFFFFF8)  # cluster 0
        struct.pack_into("<I", fat_sector, 4, 0x0FFFFFFF)  # cluster 1
        struct.pack_into("<I", fat_sector, 8, 0x0FFFFFFF)  # cluster 2 (root)

        # FAT #1
        write_sector(f, fat_start, fat_sector)
        # FAT #2
        write_sector(f, fat_start + SECTORS_PER_FAT, fat_sector)

        # ================= ROOT DIRECTORY =================
        data_start = RESERVED_SECTORS + 2 * SECTORS_PER_FAT
        zero = bytes(SECTOR_SIZE)

        for i in range(SECTORS_PER_CLUSTER):
            write_sector(f, data_start + i, zero)

    print("Imagem FAT32 estilo ZIP-750 criada com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fat32_750.py zip750.img")
    else:
        main(sys.argv[1])
