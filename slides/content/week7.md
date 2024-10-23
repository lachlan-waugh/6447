---
title: "7: rop"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 18:05

---

{{< slide class="center" >}}
# return oriented programming
### 6447 week7

---

## House cleaning
{{% section %}}

### Fuzzer
* Midpoint check-in is due this Sunday 6pm
* Make sure you've got a working prototype

---

### Midterm
* How'd you find it

{{% /section %}}

---

## A summary so far
{{% section %}}

### weeks 2/3
* buffer overflow &#8594; `win()`
* shellcode (building a `win()`)

&nbsp;

### now:
* rop/ret2 (building a `win()` when NX is on)

---

### buffer overflows
* Abusing functions which can read more data than they have allocated memory for (`gets`, `strcpy`)

* Allows us to control the stack (local vars, ret)

* *Mitigations*: ASLR/PIE/Stack canaries

* *Breaking them*: leaking addresses/the canary

---

### shellcode
* Once we can control execution of the program (e.g. changing the return address), where do we go?
    * We trick it into treating our user-supplied as code.
    * Then jump to the code

* *Mitigations*: NX, buffer too small for a payload
* *Breaking them*: ROP, EggHunters

{{% /section %}}

---

{{% section %}}
## ROP
* instead of writing our own assembly instruction, we re-use existing instructions from the program.

* We use instructions preceding a `ret` (gadgets), so we can jump to them, execute them, and jump back.

* We chain these gadgets so we can execute a full payload, by: jumping to first one, executing it, jumping back, jumping to the second one, etc.

---

### how does ret work?
it grabs what rsp is pointing to, and jumps there

```
pop rcx
jmp rcx
```

> rsp is integral to our ropchain

---

### why does it jump to esp?
ret is the last thing in a function call

* it's called after:
    * local vars are cleaned up, and
    * `rbp` is grabbed off the stack
* so `rsp` should is pointing at the return address

```php
    0x18  [   ARGS   ] <- parameters
    0x14  [   RIP    ] <- +++rsp now points here+++
    0x10  [   RBP    ] <- cleaned up by leave
    0x0C  [ AAAAAAAA ] <- local vars are dealloc'd
```

---

### how does a ropchain work
it's going to execute each gadget, then grab the next one off the stack, and execute that
```php
    0x18  [ GADGET_3 ] <- parameters
    0x18  [ GADGET_2 ] <- parameters
    0x14  [ GADGET_1 ] <- +++rsp now points here+++
    0x10  [   RBP    ] <- cleaned up by leave
    0x0C  [ AAAAAAAA ] <- local vars are dealloc'd
```


---

### Gadgets
* Instructions can comprise of multiple-bytes
    * If jump to an offset within an instructions
    * We could have an entirely new instruction

```
    0xAABBCCDD          0xAABBCCDD      0xAABBCCDD
      ^^^^^^^^              ^^                ^^^^
    MOV RAX, 12         XOR RAX, RAX       INC RAX; CALL WIN
```

> note, I made those ^^^ up entirely

---

### Old shellcode
```
/* argv = envp = NULL */
xor rcx, rdx
xor rcx, rcx

/* push '/bin/sh' onto stack */
push 0x732f2f6e69622f
mov rbx, rsp

/* call execve() */
mov rax, 0xb /* Syscall Number 11 */
syscall    /* Trigger syscall */
```

---

### How do we replicate this
`execve('/bin/sh', NULL, NULL)`
```
RAX = 0x3B # (59)
RBX = address to /bin/sh
RCX = NULL
RDX = NULL
syscall
```

---

### Now that's it's ROP
Instead of raw instructions, we'll use gadgets
```
[GADGET_1] # RAX := 0x3B # (59)
[GADGET_2] # RBX := address to /bin/sh
[GADGET_3] # RCX := NULL
[GADGET_4] # RDX := NULL
[GADGET_5] # Syscall
```

---

### How do we find gadgets?
* [Ropper](https://github.com/sashs/Ropper)
* [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)
* [ropr](https://github.com/Ben-Lichtman/ropr)

---

### Finding gadgets
```
> ROPgadget --binary ropme --search 'pop rbx'
0x0804832d : pop rbx ; ret

> ROPgadget --binary ropme --search'xor rcx'
0x080484b5 : xor rcx, rcx ; ret

> ROPgadget --binary ropme --search 'xor rdx'
0x080484b8 : xor rdx, rdx ; ret

> ROPgadget --binary ropme --search 'syscall'
0x080484bb : mov rax, 0x3B ; int 0x80
```

---

### Using strings and values
`pop rbx; ret` grabs the next address on the stack, and stores it in `rbx`
```C
p32(0x08041234) // pop rbx; ret;
p32(0x0804abcd) // address of "/bin/sh"
// now rbx stores a pointer to "/bin/sh"

p32(0x08041234) // pop rbx; ret;
p32(0xA)        // 10
// now rbx == 10
```

---

### getting the stack address
we could grab the stack pointer, and store it in `rbx`
```C
push esp, pop rbx; ret;
// now rbx will store &esp
```

> generally both instructions will need to be in the same gadget

---

### What should a payload look like?
```
[  PADDING  ] <== our first gadget should overwrite ret
[  RAX=0x3B ]
[  POP RBX  ]
[  &BIN SH  ]
[  XOR RCX  ]
[  XOR RDX  ]
[  SYSCALL  ]
```

---

### How else could we get a shell?
* we can also call functions!
* what if the program already calls system?
```
CALL SYSTEM
PUSH &('/bin/sh')
```

---

### DEMO

{{% /section %}}

---

## Ret2Libc
{{% section %}}
### what if the program doesn't have (good) enough gadgets?
* we can jump to our own code
* we can also jump to any used libraries

---

* libc stores all of the useful *"builtin"* functionality (`printf`, `gets`, etc)
* that's a whole lot of gadgets we could utilise

---

* for a payload we'll need to find:
    * the base address
    * the libc version (to determine offsets)\*
    * a helpful function

> \* *function offsets vary by LIBC version, you can find the correct offsets [here](https://libc.nullbyte.cat/)*

---

### pwntools
* alternatively, you can do it with `pwntools`
* similar to setting binary base, you set the libc base
```python
libc = ELF("libc_version.so")
libc.address = printf_leak - libc.symbols['printf']
# libc.address is now the correct address

# you can directly access functions like:
libc.symbols['system'] # etc...
```

---

### helpful stuff
* you can search for stuff in pwntools
* use the functions elf.search() and next()
```python
elf = ELF('binary_file')
# you can find strings
next(elf.search(b'/bin/sh'))

# you can also find gadgets
next(elf.search(asm(b'mov rax, 0xb; ret', os='linux', arch=e.arch)))
```

---

## Demo
> ret2libc

{{% /section %}}

---

## Tutorial
> 3 chals this week, try to solve them all

---

## Walkthrough
> image-viewer?
