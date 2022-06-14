from pwn import *

# THIS IS QUESTION 2

p = process('./runner')

# read 20 bytes, then print however many bytes were read
# read stores num bytes read in eax, so put that into edx for write
payload = asm("""
    mov eax, 0x3    # eax = 3 (read)
    mov ebx, 0x0    # fd  = 0 (stdin)
    mov ecx, esp    # treat esp as a buffer, and write to it
    mov edx, 0x14   # write 0x14 == 20 bytes
    int 0x80

    mov edx, eax    # write the number of bytes written into edx (count)
    mov eax, 0x4    # eax = 4 (write)
    mov ebx, 0x1    # fd  = 1 (stdout)
    mov ecx, esp    # treat esp a buffer, and read from it
    int 0x80
""")

p.sendlineafter(b'that\n', payload)

p.interactive()
p.close()