# HELLO!

<!-- <details markdown=1>
<summary>installation</summary> -->

```python
from pwn import *

p = prog('./vulnerable-program')    # 
e = ELF('./vulnerable-program')     # 
r = remote('0.0.0.0', 1234)         # 
# https://docs.pwntools.com/en/stable/gdb.html
gdb.attach(p, )  # attach to an existing process
gdb.debug('', )   # spin up a new debugger process, stopped at the first instruction
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

<!-- </details> -->

<details>
<summary>resources</summary>
<a href="/6447/resources/pwntools"></a>
<a href="/6447/resources/pwndbg"></a>
<a href="/6447/resources/binary-ninja"></a>
<a href="/6447/resources/ida"></a>
<a href="/6447/resources/template"></a>
</details>