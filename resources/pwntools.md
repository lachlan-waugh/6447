<style>#downloads { display: none !important; }</style>

# pwntools cheatsheet

## running a program
```python
from pwn import *

r = remote('0.0.0.0', 1234) #
p = process('./vuln')          #

p.interactive() # drops you into an interactive shell
p.close()       # oh man, idk
pause()         #  
```

## debugging with gdb
```python
# https://docs.pwntools.com/en/stable/gdb.html
gdb.attach(p, gdb_cmd)  # attach to an existing process
gdb.debug('./vuln', )   # spin up a debugger process, stopped at the first instruction
```

```python
p.recvuntil(until)  # read input from p until 'line'
p.sendline(line)    # sends the line to the program
p.sendlineafter(until, line)   # combines recvuntil() and sendline()
```

## packing data
```python
p32(0x12345678)          # packs a 32-bit hex number (b'\x78\x56\x34\x12')
u32(b'\x78\x56\x34\x12') # unpacks a 32-bit (little-endian) number.
hex()           #
bytes()         #
f''.encode()    #
b''.decode()    # 
```

## shellcode
```python
asm("""
    push 0x0068732f
    push 0x6e69622f

    mov ebx, esp
    mov eax, 0xb
    mov ecx, 0
    mov edx, 0
    mov esi, 0

    int 0x80
""") # a simple system('/bin/sh') payload
```

## reading memory address
magic numbers are bad, use these instead
```python
elf = ELF('./vuln')         # 
elf = p.elf                 # same as ELF('./vuln')

elf.symbols['win']  # 
elf.got['puts']     # 

# if ASLR is enabled, you'll need to specify the binary base), otherwise it'll just give you the offset
elf.address = 0xdeadbeef 
```

## locating what part of your input overwrites certain registers
```python
c = cyclic_gen()
c.get(n)        # Get a chunk of length n
c.find(b'caaa') # -> (8, 0, 8): position 8, which is chunk 0 at position 8
```

## finding ROPTools
```python
# you can ignore this until week05
rop = ROP('./vuln') #
## TODO https://docs.pwntools.com/en/stable/rop/rop.html
```