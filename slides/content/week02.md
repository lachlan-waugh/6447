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
* AX is actually the bottom half of EAX (it's AH and AL), not the top half
![](/assets/img/week02/registers.png)

---

## stack frames
![](/assets/img/week02/stack-grows-up.png)
* what register stores the stack pointer, and frame pointer?
* Why are the parameters stored *below* the frame pointer?

---

## stack frames
```
    0x18  [  ARGS  ] <- Parameters
    0x14  [  EIP   ] <- Stored Return Pointer
    0x10  [  EBP   ] <- Stored Frame Pointer
    0x0C  [  AAAA  ] <- these are local vars
    0x08  [  0001  ] <- maybe an int?
    0x04  [  DDBF  ] <- maybe a pointer
    0x00  [  5844  ] <- maybe 2 characters
```

---

## actually it grows down
The stack grows from high address to low addresses
![](/assets/img/week02/stack-grows-down.png)

---

{{% /section %}}

---

{{% section %}}

## buffer overflows

---

## demo

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
They save the day and make everything impossible to crack! :)

* a random value placed between the user buffers and [ER]IP
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
> the real value is stored somewhere else, and is checked before the function returns

---

## how do I defeat them
memory leaks basically

* leak a function pointer, then just offset to other functions(:wave: PIE/ASLR)
* leak the canary's value (:wave: stack canaries:)

{{% /section %}}

---

## lab
* there is one binary, with 2 vulnerabilities (both trivial)
    * don't look at the source code, later on you won't be given it!
    * hop into groups of 2, give it a shot!

---

# walkthrough
