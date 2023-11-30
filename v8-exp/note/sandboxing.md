# V8 - Sandboxing (Windows):

## General:
- Divided into 2 processes broker(privilaged process - browser) and the target(sandboxed process - renderer). 
- Broker:
    - Specify policy for the target process.
    - Sandbox the taget process.
    - make sure to live while any target process is alive.
- Target:
    - make sure the process is sandboxed.
    - all outgoing ipc calls are checked before actually sent(speed optimization).

## Mitigations:
- ASLR is ON for all the imags in a process.
- Terminate the entire process on heap corruption.
- bottum-up ASLR, higher entropy to make sure its really random :D
- immediately raise an error on bad handle refernce.
- Selectively remove system calls: reduces the kernel attack surface.
- CFG: CFG security in microsoft system to make sure there is no control flow hijacking.
- CET: shadow stack to prevent hijacking the return pointer on the stack (to kill ROP attacks).
- and many more mitigations...

## refs:
- https://chromium.googlesource.com/chromium/src/+/HEAD/docs/design/sandbox.md