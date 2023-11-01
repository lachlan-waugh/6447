---
title: "03: shellcode"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 18:05

---

{{< slide class="center" >}}
# shellcode
### 6447 week03 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

{{% section %}}

## todo
* reverse engineering
* shellcode
* memory protections (again)

---

### harder re
instructions can give context to the variables

![](/assets/img/week03/operation_implications.png)

---

### harder re #2
what's different between these instructions?

```
    mov eax, dword ptr [esp]
    mov eax, word ptr [esp]
    mov eax, byte ptr [esp]
    mov ax, [esp]
    mov al, [esp]
```

---

### finding offsets
some people seemed to be confused

* binja: var\_30 means the variable is 0x30 (48) bytes away from the return address
* assembly: variable ebp-0x2B means it's 0x2B (44) bytes away from stored EBP

{{% /section %}}

---

{{% section %}}

## buffer overflows

---

### last week recap
* last week we had a nice win() function to jump to

* so we overwrite EIP with that function pointer

```php
win is at 0xDEADBEEF. gimme some data though
> AAAAAAAAAAAAAAAAAAA\xEF\xBE\xAD\xDE

wait how'd you get here?
$ rm -rf /*
```

---

### last week recap 
what does it look like in memory

```php
    0x18  [   ARGS   ] 
    0x14  [ DEADBEEF ] <- EIP
    0x10  [ 41414141 ] <- EBP
    0x0C  [ 41414141 ] 
    0x08  [ 41414141 ]
    0x04  [ 41414141 ]
    0x00  [ 41414141 ] <- our buffer
```

---

### some suggestions
dont hardcode stuff

```python
payload = fit({10: b'abcd', 100: b'efgh'}, filler=b'A')

# kinda equivalent to
payload = b'A' * 10
payload += b'abcd'
payload += b'A' * (100 - len(payload))
payload += b'efgh

# but much more readable
```

---

### why wasn't this taught last week
you should understand what the tooling does

* there's a lot the tooling can do
* but it's important to understand the fundamentals of why
* e.g. `shellcraft.i386.linux.sh()`
* don't use it

---

### but now, there is no win function
* so we can't jump to a win function anymore
* so what if we just write our own win function?

> programming in my security??

{{% /section %}}

---

{{% section %}}

## shellcode

---

### 🐚shellcode
* Q: What is a win() function (or any function)?

---

### 🐚shellcode
* Q: what is a win() function (or any function)?
* A: it's just a sequence of assembly instructions

---

### 🐚shellcode
* Q: what is a win() function (or any function)?
* A: it's just a sequence of assembly instructions
    * assembly is just bytes

---

### 🐚shellcode
* Q: what is a win() function (or any function)?
* A: it's just a sequence of assembly instructions
    * assembly is just bytes
    * bytes is just data (which we can send)

---

### 🐚shellcode
* Q: what is a win() function (or any function)?
* A: it's just a sequence of assembly instructions
    * assembly is just bytes
    * bytes is just data (which we can send)
* if we write some assembly instructions, and point EIP at them, we can  get code execution (e.g. read/write, pop a shell)!

---

### what does this like look
in memory

```php
    0x48  [   ARGS   ] < 
    0x44  [ 00000030 ] <- EIP
    0x40  [ AA094101 ] <- hacks nasa? 
    0x3C  [ 12350ADA ] <- calls back to a c2
    0x38  [ 48392918 ] <- deploys malware on the system
    0x34  [ 59059474 ] <- pops a shell
    0x30  [ 56486420 ] <- our buffer
```

---

### some helpful instructions :)
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

---

### what is a syscall
* we don't have privilege to perform certain actions, but the kernel does
    * e.g. reading/writing, networking, creating processes 
* a syscall is kinda like a kernel API to invoke these services on our behalf

---

### idc, how do we /bin/sh
basically this

```
eax = 0xB (11)
ebx = char __user *
ecx = char __user * __user *
edx = char __user * __user *
esi = struct pt_regs *
```

---

### most of those don't matter
this is how you invoke `/bin/sh`

```
eax = OxB (important, the sycall number)
ebx = *("/bin/sh") (important, this is the program to run) 
ecx = NULL (not important, this is arguments to that program)
edx = NULL (not important, this is environment variables)
esi = NULL (not important, idk what this is)
```

---

### so how do we do that
one example

```
mov eax, 0xB        # eax = 12
mov ebx, 0x8041234  # imagine that is the pointer to /bin/sh
xor ecx, ecx        # ecx = NULL
xor edx, edx        # edx = NULL
xor esi, esi        # esi = NULL

int 0x80            # invoke syscall
```

---

{{% /section %}}

---

## demo
* poppin a shell with ./runner

---

{{% section %}}

## my payload isn't working, help
* no /bin/sh's?
* NOPNOPNOPNOPNOPNOP
* egghunters

---

## The /bin/sh problamo
/bin/sh\00 
```
                ↓↓ that's a null byte :(
 hs/  |  push 0x0068732F
nib/  |  push 0x6E69622F    
```

&nbsp;

* what if:
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

> However, what happens to our null byte?

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

## alternatively

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

## why does that work?
* `call func` will push the return address (the address of the next instruction) onto the stack

* the return address of `call pwn` would be &pwn

* now we have the address of `pwn`, we just need to offset to `binsh`, and use that as our address

source: [here](https://www.aldeid.com/wiki/X86-assembly/Instructions/call)

---

# alternatively #2
* all of the strings in the program are still accessible to you
* so you could just feed their address in (if any of them are useful of course).

{{% /section %}}

---

{{% section %}}
# NOPNOPNOP

---

### nopsledin' away
sometimes 
* we don't know exactly where our payload will be, or
* the address is a random distance into our buffer.

&nbsp;

```
the start of our input             the leaked address
↓↓↓↓                               ↓↓↓↓
\xDE \xAD \xBE \xEF \xCA \xFE \xBA \xBE \xTR \xIV \xIA \xLl
```

---

### nopsledin' away
`nop` (no-operation) `\x90` is a single-byte instruction, which does nothing

&nbsp;

So what if we padded our input out with those `nops` (similar to padding we used to reach EIP)

```
the start of our input             the leaked address
↓↓↓↓                               ↓↓↓↓
\x90 \x90 \x90 \x90 \x90 \x90 \x90 \xDE \xAD \xBE \xEF \xCA \xFE
```

---

### what if no nop
sometimes you might get WAFed

* if `\x90` (NOOP) is blocked
* you can just use something else e.g. `xchg eax, eax`
* or any meaningless (for your use) one-byte instruction

{{% /section %}}

---

{{% section %}}

## 🥚 egghunter
* Q: what if our buffer isn't big enough for a payload?

---

## 🥚 egghunter
* Q: what if our buffer isn't big enough for a payload?
    * if we have a big non-overflowable buffer, we can store the payload there (and an egg).

---

## 🥚 egghunter
* Q: what if our buffer isn't big enough for a payload?
    * if we have a big non-overflowable buffer, we can store the payload there (and an egg).
    * then in our overflowable buffer, we put a small payload which will search for & execute the egg.

---

## 🍳 omelette egghunter
* Q: what if we don't any buffer big enough?

---

## 🍳 omelette egghunter
* Q: what if we don't any buffer big enough?
* A: if we have a number of small buffers
    * store a bit of the payload in each buffer

---

## 🍳 omelette egghunter
* Q: what if we don't any buffer big enough?
* A: if we have a number of small buffers
    * store a bit of the payload in each buffer
    * use the egghunter to find each of those eggs.

---

## 🍳 omelette egghunter
* Q: what if we don't any buffer big enough?
* A: if we have a number of small buffers
    * store a bit of the payload in each buffer
    * use the egghunter to find each of those eggs.
    * chain their execution, to execute our full payload.

{{% /section %}}

---

## tutorial
now it's your turn!
* {{% fragment %}}Print "hello world\n" to stdout.{{% /fragment %}}
* {{% fragment %}}Print a user entered string (from stdin) to stdout.{{% /fragment %}}
* {{% fragment %}}Open a file 'flag.txt', read 10 bytes from it, print them, and close the file{{% /fragment %}}
* {{% fragment %}}Transcribe the given code into assembly{{% /fragment %}}

---

## walkthrough
