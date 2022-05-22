# HELLO!

```python
from pwn import *

p = prog('./vuln')          # 
e = ELF('./vuln')           # 
r = remote('0.0.0.0', 1234) #

# https://docs.pwntools.com/en/stable/gdb.html
gdb.attach(p, gdb_cmd)  # attach to an existing process
gdb.debug('./vuln', )   # spin up a debugger process, stopped at the first instruction
```

```python
p.interactive()     # drops you into an interactive shell
p.close()           # gee idk
```

```python
p.recvuntil(until)  # read input from p until 'line'
p.sendline(line)    # sends the line to the program
p.sendlineafter(until, line)   # combines recvuntil() and sendline()
```

```python
p32(0x12345678) # packs a 32-bit hex number (e.g. 0x12345678 -> b'\x78\x56\x34\x12')
```