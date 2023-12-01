# Heap based exploitation

These are different types of heap attacks.

| topics | description |
| --- | --- |
|[fastbin attack - 1](./general/fastbin/) | we create a fake fastbin in the __malloc_hook region to make it point to one_gadget | 
|[fastbin attack - 2](./general/fastbinagain/) | another fastbin challenge for practice | 
|[unlink attack](./general/unlink/) | We abuse the unlink function to write to the ret addr to jump to the win function. |
|[house of attacks*](./houses/) | will be updating more house of attacks* |
|[malloc labs](./malloclab-handout/) | create your own malloc :D |
|[tcache based attacks](./tcache/) | heap overflow to control the tcache list | 
|[tcache poisoning](./tcache/tcache_poisoning/) | defeating safe linking and tampering tcache chunks metadata | 
|[FSOP](./FSOP/) | File structure exploitation and vtable hijacking | 
<br>

Starting out resources:

* https://github.com/shellphish/how2heap
* https://heap-exploitation.dhavalkapil.com/
* https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/
* https://niftic.ca/posts/fsop/