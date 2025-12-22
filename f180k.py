SECTOR = 512
TOTAL_SECTORS = 360
print("\033c\033[40;37m\ngive me a file name ? ")
i=input().strip()

with open(i, "wb") as f:
    f.write(b'\x00' * SECTOR * TOTAL_SECTORS)

print("Imagem 180 KB criada")

boot = bytearray(512)

boot[0:3]   = b'\xEB\x3C\x90'
boot[3:11]  = b'MSDOS3.3'
boot[11:13] = (512).to_bytes(2, 'little')
boot[13]    = 2              # setores por cluster
boot[14:16] = (1).to_bytes(2, 'little')
boot[16]    = 2              # FATs
boot[17:19] = (64).to_bytes(2, 'little')
boot[19:21] = (360).to_bytes(2, 'little')
boot[21]    = 0xFC           # media descriptor
boot[22:24] = (2).to_bytes(2, 'little')
boot[24:26] = (9).to_bytes(2, 'little')
boot[26:28] = (1).to_bytes(2, 'little')
boot[510:512] = b'\x55\xAA'

with open(i, "r+b") as f:
    f.seek(0)
    f.write(boot)