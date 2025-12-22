k=1024
root_dir_size = 360 * k  # entradas * tamanho
root = b'\x00' * root_dir_size

root_offset = 512 * (1 + 2 + 2)  # boot + FATs
boot = bytearray(512)

print("\033c\033[40;37m\ngive me the name of new file ? ")
i=input().strip()

with open(i, "wb") as f:
    f.write(root)


boot[0:3] = b'\xEB\x3C\x90'
boot[3:11] = b'MSDOS5.0'
boot[11:13] = (512).to_bytes(2, 'little')
boot[13] = 2                # setores por cluster
boot[14:16] = (1).to_bytes(2, 'little')   # reservados
boot[16] = 2                # FATs
boot[17:19] = (112).to_bytes(2, 'little') # root entries
boot[19:21] = (720).to_bytes(2, 'little') # setores totais
boot[21] = 0xFD             # media descriptor
boot[22:24] = (2).to_bytes(2, 'little')   # setores por FAT
boot[24:26] = (9).to_bytes(2, 'little')   # setores por pista
boot[26:28] = (2).to_bytes(2, 'little')   # cabeças
boot[510:512] = b'\x55\xAA'

with open(i, "r+b") as f:
    f.seek(0)
    f.write(boot)




