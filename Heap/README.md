# Heap based exploitation

Heap Exploitation, This exploitation mainly focus on bad implementations of malloc(Dynamic Memory Allocator) usually by the developer of a specific software. Major bug class as most softwares use Dynamic Memory.

| CMU Lab | description |
| --- | --- |
|[malloc labs](./malloclab-handout/) | Before Delving into heap exploit, create your own implementation for malloc. |

| Fastbin | description |
| --- | --- |
|[Fake fastbin](./general/fastbin/) | we create a fake fastbin in the __malloc_hook region to make it point to one_gadget | 
|[Practice: Fastbin](./general/fastbinagain/) | another fastbin challenge for practice | 

| House of * | description |
| --- | --- |
|[justCTF: house](./../ctf/justCTF/house/)| Basic form of House of Force attack is used here.|
|[house of attacks*](./houses/) | Few house of `Attacks` I have done. |

| General Bug Class | description |
| --- | --- |
|[Unlink attack](./general/unlink/) | We abuse the unlink function to write to the ret addr to jump to the win function. |
|[Heap Overflow](./general/heap-Overflow/got-overwrite/) | We take advantage of a heap Overflow to leak libc and over write the GOT table. HTB Challenge |
|[UAF: crewCTF](./../ctf/crewCTF23/company/) | Heap UAF alongside seccomp, so have to do some ROP misc to leak the file names and print those contents. |

| Tcache | description |
| --- | --- |
|[bluehens](./tcache/bluehens2022/) | Heap overflow to tcache poisoning with Safe linking enabled. | 
|[brain-f*ck](./tcache/csaw-finals/) | OOB due to bad implementation of the `brainf*ck interpreter`. | 
|[tcache stashing](./../ctf/umdctf/chisel/)| Basic Usage of stashing the smallbins into the tcache. |
|[practice Chall](./tcache/dc-quals-babyheap/) | Simple tcache attack. | 
|[tcache poisoning](./tcache/tcache_poisoning/writeup.md) | Writeup on how to do tcache poisoning. Not a challenge | 

| File Stream Exploitation | description |
| --- | --- |
|[FSOP Category](./FSOP/) | File structure exploitation and vtable hijacking | 
|[stdout - leaks](./../ctf/umdctf/ornithopter/) | Abusing bss OOB indexing - FSOP stack leak - ROP |

| Hard Challs | description |
| --- | --- |
|[HTB: runic, Hard](./../ctf/htb/runic/) | Custom Hash function has a bug, pretty intresting challenge. Combined with a libc GOT overwrite. | 

<br>

Starting out resources:

* https://github.com/shellphish/how2heap
* https://heap-exploitation.dhavalkapil.com/
* https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/
* https://niftic.ca/posts/fsop/