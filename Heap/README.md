# Heap based exploitation

These are different types of heap attacks.

| topics | description |
| --- | --- |
|[malloc labs](./malloclab-handout/) | Before Delving into heap exploit, create your own malloc :D |
|[justCTF: house](./../ctf/justCTF/house/)| Basic form of House of Force attack is used here.|
|[got overwrite](./general/heap-Overflow/got-overwrite/) | We take advantage of a heap Overflow to leak libc and over write the GOT table. HTB Challenge |
|[fastbin attack - 1](./general/fastbin/) | we create a fake fastbin in the __malloc_hook region to make it point to one_gadget | 
|[fastbin attack - 2](./general/fastbinagain/) | another fastbin challenge for practice | 
|[unlink attack](./general/unlink/) | We abuse the unlink function to write to the ret addr to jump to the win function. |
|[house of attacks*](./houses/) | Few house of Attacks. |
|[crewCTF: company](./../ctf/crewCTF23/company/) | Heap UAF alongside seccomp, so have to do some ROP misc to leak the file names and print those contents. |
|[tcache based attacks](./tcache/) | heap overflow to control the tcache list | 
|[tcache poisoning](./tcache/tcache_poisoning/) | defeating safe linking and tampering tcache chunks metadata | 
|[tcache stashing](./../ctf/umdctf/chisel/)| Basic Usage of stashing the smallbins into the tcache. |
|[FSOP](./FSOP/) | File structure exploitation and vtable hijacking | 
|[HTB: runic, Hard](./../ctf/htb/runic/) | Custom Hash function has a bug, pretty intresting challenge. Combined with a libc GOT overwrite. | 

<br>

Starting out resources:

* https://github.com/shellphish/how2heap
* https://heap-exploitation.dhavalkapil.com/
* https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/
* https://niftic.ca/posts/fsop/