# 32 bit ret2libc - silver_bullet

```python
struct bullet {
    char[48] description;
    uint power;
}
```

- We have to overflow the description and then make the power big to defeat the werewolf.

## Issue:

```python
strncat((char *)bullet,input_buf,0x30 - bullet->power);
```

- strncat will concatenate n+1 bytes including the null character.
- So give 48 bytes(max length) and make it overflow to the power variable. We can write more on the stack. Since this is 32 bit arch we can give all the return address and its parameters in the stack.

### Ret2libc:

- call puts@plt with puts@got so that we can leak a libc function(puts).
- Now we calculate the libc address and find out the address of /bin/sh and system() and then call system with “/bin/sh” as argument.
