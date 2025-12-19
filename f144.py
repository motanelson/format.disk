boot_sector = bytearray(512)

# Jump + OEM
boot_sector[0:3] = b'\xEB\x3C\x90'
boot_sector[3:11] = b'MSDOS5.0'

# Bytes por setor
boot_sector[11:13] = (512).to_bytes(2, 'little')

# Setores por cluster
boot_sector[13] = 1

# Setores reservados
boot_sector[14:16] = (1).to_bytes(2, 'little')

# Número de FATs
boot_sector[16] = 2

# Entradas de root
boot_sector[17:19] = (224).to_bytes(2, 'little')

# Total de setores
boot_sector[19:21] = (2880).to_bytes(2, 'little')

# Media descriptor (F0 = disquete)
boot_sector[21] = 0xF0

# Setores por FAT
boot_sector[22:24] = (9).to_bytes(2, 'little')

# Setores por trilho
boot_sector[24:26] = (18).to_bytes(2, 'little')

# Cabeças
boot_sector[26:28] = (2).to_bytes(2, 'little')

# Assinatura boot
boot_sector[510:512] = b'\x55\xAA'
print("\033c\033[40;37m\nget me the file name ? ")
i=input().strip()
with open(i, "wb") as f:
    f.write(boot_sector)
    f.write(b"\x00" * (1474560 - 512))

print("Imagem FAT12 1.44MB criada.")

