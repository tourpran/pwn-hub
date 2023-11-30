; tiny.asm
BITS 32
EXTERN _exit
GLOBAL _start
SECTION .text
_start:
    mov al, 0xb
    push 0x68732f2f
    push 0x6e692f2f
    mov ebx, esp
    int 0x80