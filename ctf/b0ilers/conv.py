from pwn import *

pi = 3.141592653589793
e = 2.718281828459045

x = pi-e

print(x, hex(struct.unpack('<Q', struct.pack('<d', x))[0]))


from ctypes import pointer, memmove, c_ulonglong, c_double
x = c_double(x)
y = c_ulonglong()
memmove(pointer(y),pointer(x),8)
print(hex(y.value))