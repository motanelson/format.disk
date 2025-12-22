import struct
DISK_SIZE = 720 * 1024  # 737280 bytes
SECTOR_SIZE = 512

def escrever_boot_sector(f):
    bs = bytearray(512)

    bs[0:3] = b'\xEB\x3C\x90'      # JMP
    bs[3:11] = b'MSDOS5.0'
    bs[11:13] = struct.pack("<H", 512)
    bs[13] = 2                    # sectors per cluster
    bs[14:16] = struct.pack("<H", 1)  # reserved
    bs[16] = 2                    # FATs
    bs[17:19] = struct.pack("<H", 112)
    bs[19:21] = struct.pack("<H", 1440)  # total sectors
    bs[21] = 0xF9                 # media descriptor
    bs[22:24] = struct.pack("<H", 3)  # sectors per FAT
    bs[24:26] = struct.pack("<H", 9)
    bs[26:28] = struct.pack("<H", 2)
    bs[28:32] = struct.pack("<I", 0)
    bs[510:512] = b'\x55\xAA'

    f.seek(0)
    f.write(bs)


def criar_imagem_720k(nome):
    with open(nome, "wb") as f:
        f.write(b'\x00' * DISK_SIZE)
        escrever_boot_sector(f)

    print("Imagem 720K criada:", nome)

if __name__ == "__main__":
    print("\033c\033[40;37m\nget me the file name ? ")
    i=input().strip()
    criar_imagem_720k(i)
    