---
title: "Week07"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# Week07
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

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

### Weeks 2/3
* buffer overflow &#8594; `win()`
* shellcode (building a `win()`)

&nbsp;

### Now:
* ROP (building a `win()` again)

---

### Buffer overflows
* Abusing functions which can read more data than they have allocated memory for (`gets`, `strcpy`)

* Allows us to control the stack (local vars, ret)

* *Mitigations*: ASLR/PIE/Stack canaries

* *Breaking them*: leaking addresses/the canary

---

### Shellcode
* Once we can control execution of the program (e.g. changing the return address), where do we go?
    * We trick it into treating our user-supplied as code.
    * Then jump to the code

* *Mitigations*: NX, buffer too small for a payload
* *Breaking them*: ROP, EggHunters

{{% /section %}}

---

## ROP
{{% section %}}
* Instead of writing our own assembly instruction, we re-use existing instructions from the program.

* We use instructions preceding a `ret` (gadgets), so we can jump to them, execute them, and jump back.

* We chain these gadgets so we can execute a full payload, by: jumping to first one, executing it, jumping back, jumping to the second one, etc.

---

### Gadgets
* Instructions can comprise of multiple-bytes
    * If jump to an offset within an instructions
    * We could have an entirely new instruction

```
    0xAABBCCDD          0xAABBCCDD      0xAABBCCDD
      ^^^^^^^^              ^^                ^^^^
    MOV EAX, 12         XOR EAX, EAX       INC EAX; CALL WIN
```

> note, I made those ^^^ up entirely

---

### Old shellcode
```
/* argv = envp = NULL */
xor edx, edx
xor ecx, ecx

/* push '/bin/sh' onto stack */
push 0x68
push 0x732f2f2f
push 0x6e69622f
mov ebx, esp

/* call execve() */
mov eax, 0xb /* Syscall Number 11 */
int 0x80     /* Trigger syscall */
```

---

### How do we replicate this
`execve('/bin/sh', NULL, NULL)`
```
EAX = 0xB # (11)
EBX = address to /bin/sh
ECX = NULL
EDX = NULL
INT 0x80 Syscall
```

---

### Now that's it's ROP
Instead of raw instructions, we'll use gadgets
```
[GADGET_1] # EAX := 0xB # (11)
[GADGET_2] # EBX := address to /bin/sh
[GADGET_3] # ECX := NULL
[GADGET_4] # EDX := NULL
[GADGET_5] # INT 0x80 Syscall
```

---

### How do we find gadgets?
* [Ropper](https://github.com/sashs/Ropper)
* [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)
* [ropr](https://github.com/Ben-Lichtman/ropr)

---

### Finding gadgets
```
> ROPgadget --binary ropme | grep 'pop ebx'
0x0804832d : pop ebx ; ret

> ROPgadget --binary ropme | grep 'xor ecx'
0x080484b5 : xor ecx, ecx ; ret

> ROPgadget --binary ropme | grep 'xor edx'
0x080484b8 : xor edx, edx ; ret

> ROPgadget --binary ropme | grep 'int 0x80'
0x080484bb : mov eax, 0xb ; int 0x80
```

---

### Using strings and values
`pop ebx; ret` grabs the next address on the stack, and stores it in `ebx`
```C
p32(0x08041234) // pop ebx; ret;
p32(0x0804abcd) // address of "/bin/sh"
// now ebx stores a pointer to "/bin/sh"

p32(0x08041234) // pop ebx; ret;
p32(0xA)        // 10
// now ebx == 10
```

---

### Getting the stack address
we could grab the stack pointer, and store it in `ebx`
```C
push esp, pop ebx; ret;
// now ebx will store &esp
```

> Generally both instructions will need to be in the same gadget

---

### What should a payload look like?
```
[  PADDING  ] <== our first gadget should overwrite ret
[  EAX=0xB  ]
[  POP EBX  ]
[  &BIN SH  ]
[  XOR ECX  ]
[  XOR EDX  ]
[  SYSCALL  ]
```

---

### How else could we get a shell?
* we can also call functions!
* what if the program already calls system?
```
CALL SYSTEM
PUSH &('/bin/sh)
```

---

### DEMO

{{% /section %}}

---

## Ret2Libc
{{% section %}}
### What if the program doesn't have (good) enough gadgets?
* We can jump to our own code
* We can also jump to any used libraries

---

* LIBC stores all of the useful *"builtin"* functionality (`printf`, `gets`, etc)
* That's a whole lot of gadgets we could utilise

---

* For a payload we'll need to find:
    * the base address
    * the libc version (to determine offsets)\*
    * a helpful function

> \* *function offsets vary by LIBC version, you can find the correct offsets [here](https://libc.nullbyte.cat/)*

---

### Pwntools
* Alternatively, you can do it with `pwntools`
* Similar to setting binary base, you set the libc base
```python
libc = ELF("libc_version.so")
libc.address = printf_leak - libc.symbols['printf']
# libc.address is now the correct address

# you can directly access functions like:
libc.symbols['system'] # etc...
```

---

## Demo
> Ret2Libc

{{% /section %}}

---

## Tutorial
> 3 chals this week, try to solve them all

---

## Walkthrough
> elon-musk
