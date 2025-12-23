boot = bytearray(512)

SECTOR_SIZE = 512
TOTAL_SECTORS = 399360
TOTAL_SIZE = TOTAL_SECTORS * SECTOR_SIZE

boot = bytearray(512)

boot[0:3] = b'\xEB\x3C\x90'
boot[3:11] = b'ZIP200  '

boot[11:13] = (SECTOR_SIZE).to_bytes(2, 'little')
boot[13] = 16                 # sectors per cluster
boot[14:16] = (1).to_bytes(2, 'little')
boot[16] = 2                  # FATs
boot[17:19] = (1024).to_bytes(2, 'little')

boot[19:21] = (0).to_bytes(2, 'little')      # must be zero
boot[21] = 0xF8                               # fixed disk
boot[22:24] = (400).to_bytes(2, 'little')    # sectors per FAT

# Fake geometry (ignored by OS)
boot[24:26] = (63).to_bytes(2, 'little')
boot[26:28] = (255).to_bytes(2, 'little')

boot[28:32] = (0).to_bytes(4, 'little')
boot[32:36] = (TOTAL_SECTORS).to_bytes(4, 'little')

boot[510:512] = b'\x55\xAA'




print("\033c\033[40;37m\nget me the file name ? ")
i=input().strip()
with open(i, "wb") as f:
    f.write(boot)
    f.write(b"\x00" * ((1024*1024*200) - 512))

print("Imagem FAT16 200.0MB criada.")

