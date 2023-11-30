from pwn import *

p = remote("mercury.picoctf.net", 22239)

code = ""
with open("./exp.js") as f:
    code = f.read()
print(code)

p.sendline(str(len(code)))
p.send(code)

p.interactive()