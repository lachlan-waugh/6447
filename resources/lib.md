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
