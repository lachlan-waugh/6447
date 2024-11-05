---
title: "2: buffer overflows"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 18:05

---

{{< slide class="center" >}}
# buffer overflowssssssssssssssssssssssssssssssssssssssssssss\xef\xeb\ad\ed
### 6447 week2

---

{{% section %}}

## stack frames
* what register stores the stack, and frame pointer?
* why are the parameters stored *below* frame pointer?

---

## the stack grows down
* the stack grows from high address to low addresses
* so the top of the stack, is lower down in memory
* this doesn't really change how you exploit, you also just write up the stack

---

## stack frames
basic example

```
    0x30  [       ARGS       ] <- parameters
    0x28  [       RIP        ] <- stored return pointer
    0x20  [       RBP        ] <- stored frame pointer
    0x18  [ AAAAAAAAAAAAAAAA ] <- local vars
    0x10  [ 0000000000000001 ] <- an int?
    0x08  [ DEADBEEFCAFEBABE ] <- a pointer
    0x00  [ 5945455459454554 ] <- 4 characters
```

---

## where are vars
referenced in relation to `rbp` e.g. `rbp-0x4`

* local vars are ~~above~~ lower, so `rbp-0x4`
* arguments are ~~below~~ higher so `rbp+0x8`

{{% /section %}}

---

{{% section %}}

## buffer overflows

---

### reading into a buffer
what happens when you write more content than a buffer can hold

* modern languages might just resize (python)
* some languages might throw an exception
* maybe it would crash? (sometimes it will)
* C (& lower-level languages) just kinda run with it

---

### overflowing
so where exactly does that content go

* we've talked about stack frames
* if we write more content, it'll just start overwriting other content on the stack
    * other variables
    * control stuff (RBP, RIP)

---

### what can I overwrite?
* local variables
* return addresses
* ~~content from other processes?~~

> this could allow us to change the application flow

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

# we SIGSEGV at RIP = EEEEEEEE
```
> then we need 16 bytes of padding before the return address

---

### how to generate random strings

pwntools
```python
cyclic(20) # generate a chunk of length 20
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

---

## PIE
position independent execution

* every time you run the binary, it gets loaded into a different location in memory
* this means just can't simply set EIP to `win()`
* binja will only show the offset from the binary base

> PIE is a binary protection

---

### what does it look like
notice the region is entirely different

```bash
# no PIE
$ ./leak
win() is at 0x08041234

# with PIE
$ ./leak
win() is at 0x05650161
$ ./leak
win() is at 0x05650911
```

---

## ASLR
address space layout randomization

> ASLR is a kernel protection

using ASLR
```bash
# turn aslr off
sudo sysctl kernel.randomize_va_space=0

# check if it's on
cat /proc/sys/kernel/randomize_va_space
```

---

## stack canaries
they save the day and make overflows impossible
* a random value between the user buffers and RIP
* if the value of that canary changes during execution, the program will abort
* this is what the `__stack_chk_fail()` thing is in some of the source code you'll have read

---

### stack canaries in memory
```
    0x30  [       ARGS       ] <- parameters
    0x28  [       RIP        ] <- stored return pointer
    0x20  [       RBP        ] <- stored frame pointer
    0x18  [ AAAAAAAAAAAAAAAA ] <- local vars
    0x10  [ 0000000000000001 ] <- an int?
    0x08  [ DEADBEEFCAFEBABE ] <- a pointer
    0x00  [ 5945455459454554 ] <- 4 characters
```

> real value stored somewhere else, and checked before the function returns

---

### how do I defeat them
memory leaks basically

* PIE/ASLR: leak function pointer and you're good
* canaries: leak the canary's value
* the stack sometimes has some interesting values, but how can we leak them (this comes in week 4)

---

### cool notes

* [these could be helpful](https://ir0nstone.gitbook.io/notes/types/stack/introduction)

{{% /section %}}
