boot = bytearray(512)
TOTAL_SECTORS = 196608
SECTOR_SIZE = 512
TOTAL_SIZE = TOTAL_SECTORS * SECTOR_SIZE

# Jump + OEM
boot[0:3] = b'\xEB\x3C\x90'
boot[3:11] = b'ZIP100  '

boot[11:13] = (512).to_bytes(2, 'little')
boot[13] = 8                    # sectors per cluster
boot[14:16] = (1).to_bytes(2, 'little')
boot[16] = 2                    # FATs
boot[17:19] = (512).to_bytes(2, 'little')

boot[19:21] = (0).to_bytes(2, 'little')      # must be 0
boot[21] = 0xF8                               # fixed disk
boot[22:24] = (250).to_bytes(2, 'little')    # sectors per FAT

boot[24:26] = (63).to_bytes(2, 'little')     # dummy
boot[26:28] = (255).to_bytes(2, 'little')    # dummy

boot[28:32] = (0).to_bytes(4, 'little')
boot[32:36] = (TOTAL_SECTORS).to_bytes(4, 'little')

boot[510:512] = b'\x55\xAA'
print("\033c\033[40;37m\nget me the file name ? ")
i=input().strip()
with open(i, "wb") as f:
    f.write(boot)
    f.write(b"\x00" * ((1024*1024*100) - 512))

print("Imagem FAT16 100.0MB criada.")

