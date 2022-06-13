from pwn import *

p = process('./runner')

# THIS IS QUESTION 4

# "You win!" = 59 6f 75 20 77 69 6e 21
payload = asm("""
## edi can be our counter variable
mov edi, 0  # counter = 0

loop:
    mov ebx, edi    # ebx can store the 
    add ebx, 0xA30  # convert int -> ASCII
    push ebx        # put ebx onto the stack

    ## printf(%d, counter)
    mov eax, 4      # eax = 4 (write)
    mov ebx, 1      # fd = 1 (fd of stdout)
    mov ecx, esp    # ecx = i
    mov edx, 2      # count = 2
    int 0x80        # SYSCALL

    ## clean up the stack
    pop ebx         # ebx = stack[TOP]

    inc edi         # ++edi
    cmp edi, 0xA    # if (i < 10)
    jl loop         # goto loop

    xor eax, eax        # eax = 0
    push eax            # push 0
    push 0xA            # push
    push 0x216e6977     # 'win!'
    push 0x20756f59     # 'You '

    ## printf(You win!)
    mov eax, 4          # eax = 4 (write)
    mov ebx, 1          # ebx = 1 (fd of stdout)
    mov ecx, esp        # ecx = You win!
    mov edx, 9          # 
    int 0x80
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()