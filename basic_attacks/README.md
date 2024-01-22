# Basic stack based attacks

These are basic stack based attacks. The binary, exploit script are given. Sometimes the source code too. Try solving them.

| topics | description |
| --- | --- |
| [ret2shellcode](https://tourpran.github.io/pwn-training/2021/05/09/simple-ret2shellcode-training1.html)| Shellcode is basically assembly instructions in thier op codes to get code excecution. |
| [ret2win: Arguments](./argument-win/) | A simple ret2win with arguments, set the arguments in registers and jump to win. |
| [ret2libc](https://tourpran.github.io/pwn-training/2021/05/24/return2libcpwntrain.html)| We jump to the library function to get arbitrary code excecution such as System. | 
| [ROP Emporium](https://ropemporium.com/) | Best place to learn the basics of Return Oriented Programming. |
| [ROP: ORW](./open_read_write/) | make a ROP chain to do open-read-write to read the flag.txt. |
| [External: SROP](https://tripoloski1337.github.io/ctf/2020/01/26/SigReturn-Oriented-Programming.html)| Sigreturn Oriented Programming, to get control over the registers and call a specific code point. |
| [bi0s: pwny racing](./pwnyracing_stack/) | we had a pwny racing in my team. (bi0s) :D. |
| [Assembly: Restricted Shellcode](./restrictive_shellcode/) | Normal shellcoding challenge with restrictions. |
| [SEECTF: TLS Canary](./mmap-note/) | getting allocation near the TLS and then leaking canary from Thread Local Storage. To do a stack based attack. |
| [laCTF: format string1](./../ctf/lactf/ret2relro/)| Easy begginer friendly format string exploitation. |
| [laCTF: format string2](./../ctf/lactf/rickroll/)| Has constraint on main being called only once. |
| [Angstrom: Harder Format String](./../ctf/angstrom/slack/)| This is Format String but a little harder, try doing this on your own if you came this far. |
| [Angstrom: Width Specifier](./../ctf/angstrom/noleek/)| Format bug exists but the output is redirected to /dev/null. |
| [Eternal: ret2dlresolve](https://syst3mfailure.io/ret2dl_resolve/)| dl_runtime_resolve is the function that helps to get the actual address of a libc function in the vmmap.|
| [RISC-v: Challenge](./smashbaby-riscv/) | Just ROP but in RISC-V architecture, nothing special.|

<br>

![roadmap](https://wiki.bi0s.in/pwning/img/pwn.png)

source: wiki.bi0s.in(roadmap), syst3mfailure(ret2resolve), tripoloski1337(SROP)