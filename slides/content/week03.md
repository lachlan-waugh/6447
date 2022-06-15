---
title: "Week03"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# week03
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

### Programming? in my security??
* Last week: jumping to a win() function
* This week: there's no win(), what do?

---

{{% section %}}


## Lecture content
* Stack frames (again)
* Harder reverse engineering
* Shellcode

---

## Stack frames (again)
```
    0x18  [  ARGS  ] <- Parameters
    0x14  [  EIP   ] <- Stored Return Pointer
    0x10  [  EBP   ] <- Stored Frame Pointer
    0x0C  [  AAAA  ] <- these are local vars
    0x08  [  AAAA  ]
    0x04  [  AAAA  ]
    0x00  [  AAAA  ]
```

---

## Harder re
![](/img/week03/operation_implications.png)

---

## Harder re #2
* what's differs between the instructions below?
```
    mov eax, dword ptr [esp]
    mov eax, word ptr [esp]
    mov eax, byte ptr [esp]
    mov ax, [esp]
    mov al, [esp]
```

{{% /section %}}

---

{{% section %}}

## 🐚 Shellcode
* Q: What is a win() function (or any function)?

---

## 🐚 Shellcode
* Q: What is a win() function (or any function)?
* A: It's just a sequence of assembly instructions

---

## 🐚 Shellcode
* Q: What is a win() function (or any function)?
* A: It's just a sequence of assembly instructions
    * Assembly is just bytes

---

## 🐚 Shellcode
* Q: What is a win() function (or any function)?
* A: It's just a sequence of assembly instructions
    * Assembly is just bytes
    * Bytes is just data (which we can send)

---

## 🐚 Shellcode
* Q: What is a win() function (or any function)?
* A: It's just a sequence of assembly instructions
    * Assembly is just bytes
    * Bytes is just data (which we can send)
* Hence if we can write some assembly instructions, and point EIP at them, we can  get code execution (e.g. read/write, pop a shell)!

---

## Some helpful instructions :)
hopefully you've seen them in 1521/MIPS?
```
    mov a, b        # a = b
    add a, value    # a += value
    sub a, value    # a -= value
    xor a, b        # a ^= b
    and a, b        # a &= b
    push a          # push a onto stack, dec esp - 4
    pop a           # pop into a from stack, add esp + 4
    int 0x80        # syscall
```
[syscall table](http://cgi.cse.unsw.edu.au/~z5164500/syscall/)

{{% /section %}}

---

{{% section %}}

## 🥚 Egghunter
Shellcode is bytes. What if there isn't enough space for a meaningful payload in an overflowable buffer?
* If we have a big non-overflowable buffer, we can store the payload there (and an egg).
* Then in our overflowable buffer, we put a small payload which will search for/execute the egg.

---

## 🍳 Omelette egghunter
What if we don't have a buffer big enough for the entire payload?
* If we have a number of small buffers
    * we use our egghunter to find each of those eggs.
    * chain their execution, to execute our full payload.

{{% /section %}}

---

## Demo
* Poppin a shell with ./runner

---

{{% section %}}

## My payload isn't working, help
* no /bin/sh's?
* NOPNOPNOPNOPNOPNOP

---

## The /bin/sh problamo
/bin/sh\00 
```
                ↓↓ that's a null byte :(
 hs/  |  push 0x0068732F
nib/  |  push 0x6E69622F    
```

&nbsp;

* What if:
    * the program stops reading at a null byte/newline?
    * the program strips/parses them out?

---

## The /bin/sh solutiomo
* Pad out /bin/sh -> /bin//sh
```
                ↓↓ that's not a null byte :)
hs//  |  push 0x68732F2F
nib/  |  push 0x6E69622F    
```

&nbsp;

* However, what happens to our null byte?

---

## The missing nullbyte
We still need to get a nullbyte onto the stack, otherwise it'll just do
```
execve('/bin//sh + <some_garbage_data>')
```

&nbsp;

There's plenty of ways to do it, e.g.
```
xor eax, eax
push eax
```

---

## Alternatively

```
call pwn
    pwn:
    pop ebx                 # ebx now stores &(pwn)
    diff = binsh - pwn      # we find the offset to binsh
    add ebx, diff           # we add the offset
    ## equivalently: lea ebx, [ebx + binsh - pwn]

    ## now ebx stores &binsh, so we call execve or w/e

    binsh: .string "/bin/sh"
```

full payload [here](https://github.com/lachlan-waugh/6447/blob/main/demos/labs/week03/shell-alternate.py)

---

## Why does that work?
* `call func` will push the return address (the address of the next instruction) onto the stack

* the return address of `call pwn` would be &pwn

* now we have the address of `pwn`, we just need to offset to `binsh`, and use that as our address

source: [here](https://www.aldeid.com/wiki/X86-assembly/Instructions/call)

---

# Alternatively #2
* All of the strings in the program are still accessible to you
* so you could just feed the addresses strings in (if any of them are useful of course).

---

# NOPNOPNOP

---

## nopsledin' away
Sometimes 
* we won't be given the exact address of the start of our payload, or
* the address is a random distance into our buffer.

&nbsp;

```
the start of our input             the leaked address
↓↓↓↓                               ↓↓↓↓
\xDE \xAD \xBE \xEF \xCA \xFE \xBA \xBE \xTR \xIV \xIA \xLl
```

---

## nopsledin' away

`nop` (no-operation) `\x90` is a single-byte instruction, which does nothing

&nbsp;

So what if we padded our input out with those `nops` (similar to padding we used to reach EIP)


```
the start of our input             the leaked address
↓↓↓↓                               ↓↓↓↓
\x90 \x90 \x90 \x90 \x90 \x90 \x90 \xDE \xAD \xBE \xEF \xCA \xFE
```

{{% /section %}}

---

## Tutorial
Now it's your turn!
* {{% fragment %}}Print "hello world\n" to stdout.{{% /fragment %}}
* {{% fragment %}}Print a user entered string (from stdin) to stdout.{{% /fragment %}}
* {{% fragment %}}Open a file 'flag.txt', read 10 bytes from it, print them, and close the file{{% /fragment %}}
* {{% fragment %}}Transcribe the given code into assembly{{% /fragment %}}

---

## Walkthrough