---
title: "02: buffer overflows"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 1[68]:05

---

{{< slide class="center" >}}
# Buffer Overflowssssssssssssssssssssssssssssssssssssssssssss\xef\xeb\ad\ed
### 6447 week02

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---


## Lecture content
* what is stack
* buffer overflows
* memory protections

---

{{% section %}}

## register layout
* AX is the bottom half of EAX (AH/AL), not the top half

---

## stack frames
* what register stores the stack, and frame pointer?
* why are the parameters stored *below* frame pointer?

---

## stack frames
basic example

```
    0x18  [  ARGS  ] <- parameters
    0x14  [  EIP   ] <- stored return pointer
    0x10  [  EBP   ] <- stored frame pointer
    0x0C  [  AAAA  ] <- local vars
    0x08  [  0001  ] <- an int?
    0x04  [  DDBF  ] <- a pointer
    0x00  [  5844  ] <- 4 characters
```

---

## actually it grows down
The stack grows from high address to low addresses

> but this doesn't really change how you exploit, you also just write up the stack

{{% /section %}}

---

{{% section %}}

## buffer overflows
tldr: trust is bad

---

### reading into a buffer
what happens when you write more content than a buffer can hold

* mordern languages might just resize (python)
* some languages might throw an exception
* maybe it would crash? (sometimes it will)
* C (& lower-level languages) just kinda run with it

---

### overflowing
so where exactly does that content go

* we've talked about stack frames
* if we write more content, it'll just start overwriting other content on the stack
    * other variables
    * control stuff (EBP, EIP)

---

### what can I overwrite?
* local variables
* return addresses
* ~~content from other processes?~~

> this could allow us to change the application flow

---

### demo

---

### when is a program vulnerable
what functions cause buffer overflows?

```C
char buffer[32] a;

// read content
gets(a);
fgets(a, 0x32, stdin)

// printf, but write to a string not stdout
sprintf(a, "%s %s %d", some, random, vars);
snprintf(a, "%s %s %d", 0x32, and, more, vars);
```

---

### but that's not all
it's not just reading content, but also copying?

```C
char buffer[32] a, buffer[64] b;

// copy contents of b into a 
strcpy(a, b);
strncpy(a, b, 64);

// append contents of b onto a
strcat(a, b);
strncat(a, b, strlen(a) + strlen(b));
```

{{% /section %}}

---

{{% section %}}

## how do I find offsets

---

### binja
binja is really nice and tells us the distance

![](../assets/img/week02/binja.png)

* int is 0xC (12) bytes away from the return address
* buffer is 0x34 (52) bytes away

> if we wrote 40 bytes of padding, and one additional byte into the buffer, we would overwrite the int

---

### cyclic
kinda like bruteforce but smart

* what if we gave a random string as input
* then found what part of the string overwrote EIP

```bash
# gets(buffer)
$ AAAABBBBCCCCDDDDEEEEFFFF

# we SIGSEGV at EIP = EEEE
```
> then we need 16 bytes of padding before the return address

---

### how to generate random strings

pwntools
```python
#  
cyclic(20) # generate a chunk of length 20

#   
c = cyclic_gen()
c.get(n)        # get a chunk of length n
c.find(b'caaa') # (8,0,8): pos 8, which is chunk 0 at pos 8
```

bash
```bash
# you can also do it on commandline
cyclic 12      # aaaaaaabaaac
cyclic -l aaab # -> 1  = find chunk
cyclic -o aaae # -> 13 = find offset
```

{{% /section %}}

---

{{% section %}}

# memory protections
ew cringe security stuff

---

## ASLR
address space layout randomization

---

## using ASLR
```bash
# turn aslr off
sudo sysctl kernel.randomize_va_space=0

# check if it's on
cat /proc/sys/kernel/randomize_va_space
```

---

## PIE
position independent execution



---

## stack canaries
they save the day and make overflows impossible

* a random value between the user buffers and [ER]IP
* if the value of that canary changes during execution, the program will abort
* this is what the `__stack_chk_fail()` thing is in some of the source code you'll have read

---

## canaries in memory
```
    0x1C  [  ARGS  ] <- parameters
    0x18  [  EIP   ] <- stored return pointer
    0x14  [ CANARY ] <- canary goes here 
    0x00  [  EBP   ] <- stored frame pointer
    0x0C  [  AAAA  ] <- these are local vars
    0x08  [  AAAA  ]
    0x04  [  AAAA  ]
    0x00  [  AAAA  ]
```
> real value is stored somewhere else, and checked before the function returns

---

## how do I defeat them
memory leaks basically

* leak a function pointer, then just offset to other functions(:wave: PIE/ASLR)
* leak the canary's value (:wave: stack canaries:)

{{% /section %}}

---

{{% section %}}

## lab
* there is one binary, with 2 vulns (both trivial)
    * don't look at the source code
    * later on you won't be given it!

> give it a go in groups of 2!

---

# walkthrough

{{% /section %}}
