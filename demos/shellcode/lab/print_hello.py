from pwn import *

# THIS IS QUESTION 1

p = process('./runner')

# hello world\n -> 68 65 6c 6c 6f 20 77 6f 72 6c 64 0A
payload = asm("""
    push 0x00000000 # 'NULL'
    push 0x0A646c72 # 'rld'
    push 0x6f77206f # 'o wo' whats this
    push 0x6c6c6568 # 'hell'

    ## printf('hello world')
    mov eax, 0x4    # eax = 4 (write)
    mov ebx, 0x1    # fd  = 1 (stdout)
    mov ecx, esp    # ecx = &(hello world)
    mov edx, 12     # edx = strlen(hello world)

    int 0x80
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()



# 



