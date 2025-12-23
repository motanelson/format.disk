#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define SECTOR_SIZE 512
#define TOTAL_SECTORS 1536000
#define RESERVED_SECTORS 32
#define SECTORS_PER_FAT 1500
#define SECTORS_PER_CLUSTER 32

void write_sector(FILE *f, uint32_t sector, const void *buf) {
    fseek(f, sector * SECTOR_SIZE, SEEK_SET);
    fwrite(buf, SECTOR_SIZE, 1, f);
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;

    FILE *f = fopen(argv[1], "wb+");
    if (!f) return 1;

    /* criar ficheiro com tamanho final */
    fseek(f, TOTAL_SECTORS * SECTOR_SIZE - 1, SEEK_SET);
    fputc(0, f);

    /* ---------------- Boot Sector ---------------- */
    uint8_t boot[SECTOR_SIZE];
    memset(boot, 0, sizeof(boot));

    boot[0] = 0xEB; boot[1] = 0x58; boot[2] = 0x90;
    memcpy(&boot[3], "ZIP750  ", 8);

    *(uint16_t*)&boot[11] = SECTOR_SIZE;
    boot[13] = SECTORS_PER_CLUSTER;
    *(uint16_t*)&boot[14] = RESERVED_SECTORS;
    boot[16] = 2;

    boot[21] = 0xF8;
    *(uint32_t*)&boot[32] = TOTAL_SECTORS;
    *(uint32_t*)&boot[36] = SECTORS_PER_FAT;

    *(uint32_t*)&boot[44] = 2;    // root cluster
    *(uint16_t*)&boot[48] = 1;    // FSInfo
    *(uint16_t*)&boot[50] = 6;    // backup boot

    boot[510] = 0x55;
    boot[511] = 0xAA;

    write_sector(f, 0, boot);

    /* ---------------- FSInfo ---------------- */
    uint8_t fsinfo[SECTOR_SIZE];
    memset(fsinfo, 0, sizeof(fsinfo));

    *(uint32_t*)&fsinfo[0]   = 0x41615252; // RRaA
    *(uint32_t*)&fsinfo[484] = 0x61417272; // rrAa
    *(uint32_t*)&fsinfo[488] = 0xFFFFFFFF;
    *(uint32_t*)&fsinfo[492] = 0xFFFFFFFF;

    fsinfo[510] = 0x55;
    fsinfo[511] = 0xAA;

    write_sector(f, 1, fsinfo);

    /* ---------------- Backup Boot ---------------- */
    write_sector(f, 6, boot);

    /* ---------------- FATs ---------------- */
    uint32_t fat_start = RESERVED_SECTORS;
    uint8_t fat[SECTOR_SIZE];
    memset(fat, 0, sizeof(fat));

    /* FAT32 entries iniciais */
    *(uint32_t*)&fat[0] = 0x0FFFFFF8; // cluster 0
    *(uint32_t*)&fat[4] = 0x0FFFFFFF; // cluster 1
    *(uint32_t*)&fat[8] = 0x0FFFFFFF; // cluster 2 (root)

    /* FAT #1 */
    write_sector(f, fat_start, fat);
    /* FAT #2 */
    write_sector(f, fat_start + SECTORS_PER_FAT, fat);

    /* ---------------- Root directory (cluster 2) ---------------- */
    uint32_t data_start = RESERVED_SECTORS + 2 * SECTORS_PER_FAT;
    uint32_t root_sector = data_start;

    uint8_t zero[SECTOR_SIZE];
    memset(zero, 0, sizeof(zero));

    for (int i = 0; i < SECTORS_PER_CLUSTER; i++)
        write_sector(f, root_sector + i, zero);

    fclose(f);
    return 0;
}

