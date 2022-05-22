<style>#downloads { display: none !important; }</style>

```markdown
# challenge-name

## Flag
FLAG{xdxd}

## General overview
1. hacked the planet x0x0
2. pwned

## Program used
```python
from pwn import *

p = remote('ip', 'port')

p.recvuntil(b'hack?')

payload = b'yes pls?'
p.sendline(payload)

p.interactive()
p.close()
\```
```